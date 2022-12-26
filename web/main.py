import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from api.urls import router as api_router
from core.config import TORTOISE_ORM, settings

app = FastAPI()

app.include_router(api_router, prefix='/api')
app.mount("/static", StaticFiles(directory="static"), name="static")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=settings.DEBUG,
    add_exception_handlers=True,
)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, log_level='info', reload=settings.DEBUG)
