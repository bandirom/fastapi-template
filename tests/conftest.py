import logging
from typing import TYPE_CHECKING, AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncTransaction,
    async_sessionmaker,
    create_async_engine,
)

from api.services.dependencies.session import get_session
from api.services.security import PasswordManager
from core import settings
from db.models import Base, User
from main import app

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

logger = logging.getLogger(__name__)

TEST_DB_SUFFIX = "_TEST"


@pytest.fixture(scope="session")
def test_db_name() -> str:
    return settings.database_uri.path.split("/")[-1] + TEST_DB_SUFFIX


@pytest.fixture(scope="session")
def test_db_uri() -> str:
    return settings.database_uri.unicode_string() + TEST_DB_SUFFIX


async def create_test_database(admin_engine, test_db_name: str):
    try:
        async with admin_engine.begin() as conn:
            await conn.execute(text(f'CREATE DATABASE "{test_db_name}"'))
        logger.debug(f"Database '{test_db_name}' created")
    except ProgrammingError:
        logger.error(f"Database '{test_db_name}' already exists, continuing...")


async def drop_test_database(admin_engine, test_db_name: str):
    async with admin_engine.begin() as conn:
        await conn.execute(
            text(
                f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{test_db_name}'
              AND pid <> pg_backend_pid()
        """
            )
        )
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{test_db_name}"'))
    logger.debug(f"Database '{test_db_name}' deleted")


@pytest.fixture(scope="session")
async def test_engine(test_db_uri, test_db_name) -> AsyncGenerator["AsyncEngine", None]:
    admin_engine = create_async_engine(
        url=settings.database_uri.unicode_string(),
        echo=True,
        isolation_level="AUTOCOMMIT",
    )
    test_engine = create_async_engine(url=test_db_uri, echo=False)
    await create_test_database(admin_engine, test_db_name)
    yield test_engine
    await admin_engine.dispose()
    await test_engine.dispose()
    await drop_test_database(admin_engine, test_db_name)


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(test_engine) -> AsyncGenerator[None, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator["AsyncSession", None]:
    _sessionmaker = async_sessionmaker(bind=test_engine, expire_on_commit=False, autocommit=False, autoflush=False)
    async with test_engine.connect() as connection:
        transaction = await connection.begin()
        async with _sessionmaker(bind=connection) as session:
            yield session
        await transaction.rollback()


@pytest.fixture(scope="function")
async def client(db_session: "AsyncSession") -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture()
async def user(db_session):
    user_data = {
        "first_name": "Margo",
        "last_name": "Robbie",
        "email": "margo.robbie@email.com",
        "password": PasswordManager().get_hashed_password('tester26'),
        "is_active": True,
    }

    stmt = insert(User).values(**user_data).returning(User)
    result = await db_session.execute(stmt)
    created_user = result.scalar_one()
    return created_user
