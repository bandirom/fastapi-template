from api.error_codes import ErrorCode


class ValidationError(Exception):
    def __init__(self, error_code: ErrorCode):
        self.code = error_code.code
        self.detail = error_code.detail

    def __str__(self):
        return self.detail
