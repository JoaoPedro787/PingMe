from fastapi import Request, Cookie, HTTPException, status, WebSocket
from starlette.requests import HTTPConnection
from typing import Annotated, Union
from config import settings
from .exceptions import TokenExpired, TokenInvalid
import jwt


def validate_user_token(
    conn: HTTPConnection,
    access_token: Annotated[str | None, Cookie()] = None,
):
    try:
        decoded = jwt.decode(
            jwt=access_token,
            algorithms=[settings.TOKEN_ALGORITHM],
            key=settings.TOKEN_KEY,
        )

        conn.state.user = decoded["user_id"]

    except jwt.ExpiredSignatureError:
        raise TokenExpired()

    except:
        raise TokenInvalid()


def get_current_user(conn: HTTPConnection):
    user = getattr(conn.state, "user", None)
    if not user:
        print("User not authenticated trying to use safe routes.")
        raise TokenInvalid()
    return user
