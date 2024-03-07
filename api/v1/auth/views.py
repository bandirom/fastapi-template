from api.v1.auth.schemas import UserSighUpSchema
from api.v1.auth.services import UserSignUpService
from db.session import SessionDep


class SignUpView:
    async def post(self, data: UserSighUpSchema, session: SessionDep):
        service = UserSignUpService(session, data)
        await service.validate()
        user = await service.create_user()
        print(f'{user=}')
        return {'detail': user.id}
