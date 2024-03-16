from fastapi import FastAPI
from fastapi.routing import APIRoute

from api.exceptions import ValidationError
from api.services.handlers import validation_exception_handler
from api.v1.routers import router as v1_router
from core import settings


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.project_name,
    openapi_url=f"/api/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(v1_router, prefix='/api/v1')
app.add_exception_handler(ValidationError, validation_exception_handler)

if __name__ == '__main__' and settings.DEBUG:
    from uvicorn import run

    run('main:app', host='0.0.0.0', port=8080, reload=True)
