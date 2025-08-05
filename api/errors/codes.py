from enum import Enum
from typing import TypedDict


class ErrorCodeT(TypedDict):
    code: str
    detail: str


class ErrorCode(Enum):
    WRONG_CREDENTIALS = ('user.auth.wrong_credentials', 'Email or password is incorrect')
    NOT_ACTIVE = ('user.auth.is_not_active', 'User is not active')
    USER_NOT_FOUND = ('user.not_found', 'User not found')
    TOKEN_EXPIRED = ('token.expired', 'Token expired')
    TOKEN_INVALID = ('token.invalid', 'Could not validate credentials')

    def __init__(self, code: str, detail: str):
        self._code = code
        self._detail = detail

    @property
    def code(self) -> str:
        return self._code

    @property
    def detail(self) -> str:
        return self._detail
