from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.services.dependencies.session import SessionDep

from .schemas import SignUpResponse, TokenResponse, UserSignUpSchema
from .services import LoginService, SignUpService


async def sign_up_view(data: UserSignUpSchema, session: SessionDep) -> SignUpResponse:
    service = SignUpService(session, data)
    await service.validate()
    user = await service.create_user()
    return SignUpResponse(id=user.id)


async def sign_in_view(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> TokenResponse:
    service = LoginService(session, form_data)
    user = await service.authenticate()
    return await service.generate_response(user)
