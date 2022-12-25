from core.security import verify_password
from models import User
from typing import Generic, Optional


class UserLogin:

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await User.filter(is_active=True).get(email=email)

    async def authenticate(self, email: str, raw_password: str):
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(raw_password, user.password):
            return None
        return user
