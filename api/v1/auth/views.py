from db.session import SessionDep

from .schemas import SignUpResponse, TokenResponse, UserSignInSchema, UserSignUpSchema
from .services import LoginService, SignUpService


async def sign_up_view(data: UserSignUpSchema, session: SessionDep) -> SignUpResponse:
    service = SignUpService(session, data)
    await service.validate()
    user = await service.create_user()
    return SignUpResponse(id=user.id)


async def sign_in_view(data: UserSignInSchema, session: SessionDep) -> TokenResponse:
    service = LoginService(session, data)
    user = await service.authenticate()
    return await service.generate_response(user)
