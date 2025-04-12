from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from . import settings

engine = create_async_engine(url=settings.database_uri.unicode_string(), echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False)
