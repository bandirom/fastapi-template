from fastapi import APIRouter

from api.auth.schemas import SignInSchema

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/sign-in")
def sign_in(data: SignInSchema):
    return {"Hello": "World"}
