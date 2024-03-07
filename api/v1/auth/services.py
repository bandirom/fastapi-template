import re
from collections import defaultdict

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.security import PasswordManager
from api.v1.auth.schemas import UserSighUpSchema
from db.models import User


class UserSignUpService:
    password_manager = PasswordManager

    def __init__(self, session: AsyncSession, data: UserSighUpSchema):
        self.session = session
        self.data = data

    async def _is_email_exists(self) -> bool:
        query = select(User).filter(User.email == self.data.email)
        result = await self.session.execute(query)
        return bool(result.scalars().first())

    async def validate_password(self) -> defaultdict[str, list]:
        errors = defaultdict[str, list](list)
        password = self.data.password
        if len(password) < 8:
            errors['password'].append("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            errors['password'].append("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            errors['password'].append("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            errors['password'].append("Password must contain at least one digit")
        if not re.search(r'[^a-zA-Z0-9]', password):
            errors['password'].append("Password must contain at least one special character")
        if self.data.password != self.data.password_confirm:
            errors['password_confirm'].append("Passwords do not match")
        return errors

    async def validate(self, raise_exception: bool = True) -> list[dict]:
        errors: list[dict] = []

        if await self._is_email_exists():
            errors.append({'email': 'User with this email already exist'})
        if password_errors := await self.validate_password():
            errors.append(password_errors)
        if errors and raise_exception:
            raise HTTPException(status_code=400, detail=errors)
        return errors

    async def create_user(self) -> User:
        self.data.password = self.password_manager().get_hashed_password(self.data.password)
        user = User(**self.data.dict())
        self.session.add(user)
        await self.session.commit()
        return user
