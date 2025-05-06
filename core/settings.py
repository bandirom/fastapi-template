import secrets
from functools import lru_cache

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings


class JwtTokenSettings(BaseModel):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 10
    ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = 'sad'
    JWT_REFRESH_SECRET_KEY: str = 'xzc'


class Settings(BaseSettings):
    database_uri: PostgresDsn
    project_name: str = 'Template'
    DEBUG: bool = False
    jwt: JwtTokenSettings = JwtTokenSettings()
    secret_key: str = secrets.token_urlsafe(32)

    class Config:
        env_nested_delimiter = "__"
        env_file = '.env'
        env_prefix = ""
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
