from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    database_uri: PostgresDsn
    project_name: str = 'Template'
    api_v1_str: str = "/api/v1"

    class Config:
        env_nested_delimiter = "__"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
