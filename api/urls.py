from fastapi import APIRouter
from .test.urls import router as test_router

router = APIRouter()

router.include_router(test_router)
