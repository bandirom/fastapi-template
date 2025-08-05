from starlette.requests import Request
from starlette.responses import JSONResponse

from api.errors.exceptions import AppException


def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
