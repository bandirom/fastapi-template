import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = 'changeMe'
    DEBUG: bool = True
    PROJECT_NAME: str = 'FastApi Template'

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


settings = Settings()
