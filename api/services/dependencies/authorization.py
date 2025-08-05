from datetime import datetime
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError

from api.errors import ErrorCode, Forbidden, NotFound
from api.services.security import JwtService
from db.models import User
from db.queries.user import UserQueryService

from .session import SessionDep

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/sign-in",
)

TokenDep = Annotated[str, Depends(reusable_oauth)]


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = JwtService().decode_token(token)
    except (JWTError, ValidationError):
        raise Forbidden(ErrorCode.TOKEN_INVALID)
    if datetime.fromtimestamp(payload.exp) < datetime.now():
        raise Forbidden(ErrorCode.TOKEN_EXPIRED)
    user = await UserQueryService(session).get_user_by_id(payload.sub)
    if not user:
        raise NotFound(ErrorCode.USER_NOT_FOUND)
    if not user.is_active:
        raise NotFound(ErrorCode.NOT_ACTIVE)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
