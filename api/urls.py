from fastapi import APIRouter

from .auth.routers import router as test_router

router = APIRouter()

router.include_router(test_router)
