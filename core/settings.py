import secrets
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import PostgresDsn, BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


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


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
