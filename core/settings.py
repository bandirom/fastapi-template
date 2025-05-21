import secrets
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings


class JwtTokenSettings(BaseModel):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 10
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = 'sad'
    JWT_REFRESH_SECRET_KEY: str = 'xzc'


class CorsSettings(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class Settings(BaseSettings):
    database_uri: PostgresDsn
    project_name: str = 'Template'
    DEBUG: bool = False
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    jwt: JwtTokenSettings = Field(default_factory=JwtTokenSettings)
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    cors: CorsSettings = Field(default_factory=CorsSettings)

    class Config:
        env_nested_delimiter = "__"
        env_file = '.env'
        env_prefix = ""
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
