from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.db import async_session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
