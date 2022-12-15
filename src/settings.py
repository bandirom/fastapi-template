import os

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


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
