from enum import Enum


class ErrorCode(Enum):
    WRONG_CREDENTIALS = (
        'user.auth.wrong_credentials',
        'Email or password is incorrect',
    )
    NOT_ACTIVE = ('user.auth.is_not_active', 'User is not active')

    def __init__(self, code: str, detail: str):
        self._code = code
        self._detail = detail

    @property
    def code(self):
        return self._code

    @property
    def detail(self):
        return self._detail
