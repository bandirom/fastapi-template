import uvicorn

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api.urls import router as api_router
from src.settings import TORTOISE_ORM

DEBUG = True
app = FastAPI()

app.include_router(api_router, prefix='/api')


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=DEBUG,
    add_exception_handlers=True,
)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, log_level='info', reload=DEBUG)
