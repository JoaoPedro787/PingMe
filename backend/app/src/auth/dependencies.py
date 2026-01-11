from fastapi import Request, Cookie, HTTPException, status
from typing import Annotated
from config import settings
from .exceptions import TokenUnauthorized
import jwt


def validate_user_token(
    request: Request, access_token: Annotated[str | None, Cookie()] = None
):
    try:
        decoded = jwt.decode(
            jwt=access_token,
            algorithms=[settings.TOKEN_ALGORITHM],
            key=settings.TOKEN_KEY,
        )

        request.state.user = decoded.user_id
    except:
        raise TokenUnauthorized()


def get_current_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise TokenUnauthorized()
    return user
