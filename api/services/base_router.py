from fastapi import APIRouter


class BaseRouter:

    def __init__(self):
        self._router = APIRouter()

    @property
    def router(self) -> APIRouter:
        return self._router

    def api_routers(self):
        pass
