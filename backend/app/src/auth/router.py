from fastapi.routing import APIRouter
from fastapi import Response
from typing import Annotated
from database import SessionDep
from config import settings
from .schemas import UserPublic, UserCreate, UserLogin
from .exceptions import UserNotFound
from .utils import format_to_datetime
from . import services


router = APIRouter()


@router.post("/sign-up", status_code=201)
def create_user(user: UserCreate, session: SessionDep):
    return services.create_user(user, session)


@router.post("/sign-in", status_code=204)
def authenticate_user(user: UserLogin, session: SessionDep, response: Response):
    """
    Handles the login endpoint.

    - Calls `authenticate_user()` service to validate credentials.
    - If valid, receives a JWT token and sends it back to the browser
      as an HTTP-only cookie.
    - Returns 204 No Content on success.

    Raises:
    - `UserNotFound()`: If the user does not exist or credentials are invalid.
    """
    access_token = services.authenticate_user(user, session)

    if not access_token:
        raise UserNotFound()

    return response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict",
        expires=format_to_datetime(type="DAY", exp=settings.COOKIE_EXP_DAY),
    )
