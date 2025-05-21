import logging

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from api.exceptions import ValidationError
from api.services.handlers import validation_exception_handler
from api.v1.routers import router as v1_router
from core import lifespan, settings

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        openapi_url=f"/api/openapi.json",
        generate_unique_id_function=custom_generate_unique_id,
        lifespan=lifespan,
    )
    application.include_router(v1_router, prefix='/api/v1')
    application.add_exception_handler(ValidationError, validation_exception_handler)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.allow_origins,
        allow_credentials=settings.cors.allow_credentials,
        allow_methods=settings.cors.allow_methods,
        allow_headers=settings.cors.allow_headers,
    )
    return application


app = get_application()


if __name__ == '__main__' and settings.DEBUG:
    from dotenv import load_dotenv
    from uvicorn import run

    load_dotenv()

    run('main:app', host='0.0.0.0', port=8080, reload=True)
