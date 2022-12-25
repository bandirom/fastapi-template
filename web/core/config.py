from pydantic import BaseSettings

from typing import NamedTuple


class Settings(BaseSettings):
    class JWT(NamedTuple):
        ACCESS_COOKIE_NAME: str = 'jwt-auth'
        REFRESH_COOKIE_NAME: str = 'refresh'
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
        REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    SECRET_KEY: str = 'changeMe'
    DEBUG: bool = True
    PROJECT_NAME: str = 'FastApi Template'


settings = Settings()


TORTOISE_ORM = {
        'connections': {
            'default': 'sqlite://db.sqlite3',
        },
        'apps': {
            'models': {
                'models': ['models', 'aerich.models'],
                'default_connection': 'default',
            },
        },
    }
