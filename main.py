from fastapi import FastAPI
from fastapi.routing import APIRoute

from core import settings
from api import router


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.project_name,
    openapi_url=f"/api/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(router, prefix='/api', tags=['api'])


if __name__ == '__main__' and settings.DEBUG:
    from uvicorn import run
    run('main:app', host='0.0.0.0', port=8080, reload=True)
