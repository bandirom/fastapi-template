from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, ValidationError
from starlette import status

from api.error_codes import ErrorCode
from api.services.security import JwtService
from core import settings
from db.models import User
from db.queries.user import UserQueryService
from db.session import SessionDep

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/sign-in",
    # scheme_name="JWT"
)
TokenDep = Annotated[str, Depends(reusable_oauth)]


class TokenPayload(BaseModel):
    sub: int
    exp: int


async def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = JwtService().decode_token(token)
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorCode.TOKEN_INVALID.to_json(),
        )
    if datetime.fromtimestamp(token_data.exp) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.TOKEN_EXPIRED.to_json(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserQueryService(session).get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.USER_NOT_FOUND.to_json())
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.NOT_ACTIVE.to_json())
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
