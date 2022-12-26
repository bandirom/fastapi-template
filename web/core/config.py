from pydantic import BaseModel, BaseSettings


class _JWT(BaseModel):
    ACCESS_COOKIE_NAME: str = 'jwt-auth'
    REFRESH_COOKIE_NAME: str = 'refresh'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


class Settings(BaseSettings):

    SECRET_KEY: str = 'changeMe'
    DEBUG: bool = True
    PROJECT_NAME: str = 'FastApi Template'
    JWT: _JWT

    class Config:
        case_sensitive = True
        env_nested_delimiter = '__'


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
