from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserQueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def is_email_exists(self, email: str) -> bool:
        query = select(User).filter(User.email == email)
        result = await self.session.execute(query)
        return bool(result.scalars().first())

    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
