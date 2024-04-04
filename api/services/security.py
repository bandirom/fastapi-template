from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from core import settings


class JwtService:
    def __init__(
        self,
        access_token_expire_minutes: int = None,
        refresh_token_expire_minutes: int = None,
        algorithm: str = None,
    ):
        self.access_token_expire = (
            access_token_expire_minutes
            or settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        self.refresh_token_expire = (
            refresh_token_expire_minutes
            or settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        self.algorithm = algorithm or settings.jwt.ALGORITHM
        self.access_token_secret_key = settings.jwt.JWT_SECRET_KEY
        self.refresh_token_secret_key = settings.jwt.JWT_REFRESH_SECRET_KEY

    def create_access_token(self, subject: str | Any) -> str:
        return self.__get_encoded_jwt(
            subject, self.access_token_expire, self.access_token_secret_key
        )

    def create_refresh_token(self, subject: str | Any) -> str:
        return self.__get_encoded_jwt(
            subject, self.refresh_token_expire, self.refresh_token_secret_key
        )

    def __get_encoded_jwt(
        self, subject: str, expires_minutes: int, secret_key: str
    ) -> str:
        expires_delta = datetime.now() + timedelta(minutes=expires_minutes)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=secret_key,
            algorithm=self.algorithm,
        )
        return encoded_jwt


class PasswordManager:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hashed_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)
