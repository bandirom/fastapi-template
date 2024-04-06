from starlette.requests import Request
from starlette.responses import JSONResponse

from api.exceptions import ValidationError


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": {"code": exc.code, "detail": exc.detail}})
