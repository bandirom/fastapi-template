from datetime import timedelta

from fastapi import APIRouter

from api.auth.schemas import SignInSchema
from api.auth.services import UserLogin
from core import security
from core.config import settings
from models import User

router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "World"}


@router.post("/sign-in")
async def sign_in(data: SignInSchema):
    users = await User.all()
    user = await UserLogin().get_user_by_email(data.email)

    access_token_expires = timedelta(minutes=settings.JWT.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
