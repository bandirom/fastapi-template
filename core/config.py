import os

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str = "secret"

    PROJECT_NAME = os.environ.get('PROJECT_NAME', 'FastAPI')

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


@AuthJWT.load_config
def get_config():
    return Settings()





settings = Settings()
