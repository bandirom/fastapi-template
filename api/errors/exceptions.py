from fastapi import status

from .codes import ErrorCode


class AppException(Exception):
    status_code: int

    def __init__(self, error_code: ErrorCode):
        self.code = error_code.code
        self.detail = error_code.detail

    def to_dict(self) -> dict:
        return {"code": self.code, "detail": self.detail}


class Unauthorized(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED


class Forbidden(AppException):
    status_code = status.HTTP_403_FORBIDDEN


class NotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND


class ValidationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
