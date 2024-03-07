from fastapi import APIRouter

from .auth import AuthRouter

router = APIRouter()

router.include_router(AuthRouter().router, prefix='/auth', tags=['auth'])
