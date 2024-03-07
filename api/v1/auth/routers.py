from fastapi import APIRouter

from api.v1.auth.views import SignUpView


class AuthRouter:

    def __init__(self):
        self._router = APIRouter()
        self.signup_view = SignUpView()
        self._router.add_api_route(
            path='/signup',
            endpoint=self.signup_view.post,
            methods=['POST'],
        )

    @property
    def router(self) -> APIRouter:
        return self._router
