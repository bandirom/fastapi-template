from api.services.base_router import BaseRouter
from api.v1.auth import views


class AuthRouter(BaseRouter):

    def __init__(self):
        super().__init__()
        self._router.add_api_route(
            path='/sign-up',
            endpoint=views.sign_up_view,
            methods=['POST'],
        )
        self._router.add_api_route(
            path='/sign-in',
            endpoint=views.sign_in_view,
            methods=['POST'],
        )
        self._router.add_api_route(
            path='/logout',
            endpoint=views.logout_view,
            methods=['POST'],
        )
