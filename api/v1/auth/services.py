import re
from collections import defaultdict

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.error_codes import ErrorCode
from api.exceptions import ValidationError
from api.services.security import JwtService, PasswordManager
from api.v1.auth.schemas import TokenResponse, UserSignUpSchema
from db.models import User
from db.queries.user import UserQueryService


class SignUpService:
    password_manager = PasswordManager

    def __init__(self, session: AsyncSession, data: UserSignUpSchema):
        self.query = UserQueryService(session)
        self.data = data

    async def _is_email_exists(self) -> bool:
        return await self.query.is_email_exists(self.data.email)

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
        user = User(**self.data.model_dump(), is_active=True)
        await self.query.create_user(user)
        return user


class LoginService:
    password_manager = PasswordManager

    def __init__(self, session: AsyncSession, data: OAuth2PasswordRequestForm):
        self.data = data
        self.query = UserQueryService(session)

    async def authenticate(self) -> User:
        user = await self.query.get_user_by_email(self.data.username)
        if not user:
            raise ValidationError(ErrorCode.WRONG_CREDENTIALS)
        if not self.password_manager().verify_password(self.data.password, user.password):
            raise ValidationError(ErrorCode.WRONG_CREDENTIALS)
        if not user.is_active:
            raise ValidationError(ErrorCode.NOT_ACTIVE)
        return user

    async def generate_response(self, user: User) -> TokenResponse:
        service = JwtService()
        access_token = service.create_access_token(user.id)
        refresh_token = service.create_refresh_token(user.id)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
