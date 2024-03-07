from fastapi import APIRouter
from .v1 import routers as v1_routers


router = APIRouter()

router.include_router(v1_routers.router, prefix='/v1')
