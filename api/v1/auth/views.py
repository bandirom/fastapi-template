from db.session import SessionDep

from .schemas import UserSignInSchema, UserSignUpSchema
from .services import LoginService, SignUpService


async def sign_up_view(data: UserSignUpSchema, session: SessionDep):
    service = SignUpService(session, data)
    await service.validate()
    user = await service.create_user()
    return {'detail': user.id}


async def sign_in_view(data: UserSignInSchema, session: SessionDep):
    service = LoginService(session, data)
    user = await service.authenticate()
    return await service.generate_response(user)
