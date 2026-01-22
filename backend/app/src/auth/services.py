from pwdlib import PasswordHash
from sqlmodel import select, or_
from .models import User
from .utils import format_to_datetime
from config import settings
import jwt

password_hash = PasswordHash.recommended()


def create_user(user, session):

    hashed_password = password_hash.hash(user.password)

    # Removing field password and adding hashed_password
    user = user.model_dump(exclude={"password"})
    user["hashed_password"] = hashed_password

    user_db = User(**user)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


def authenticate_user(user, session):
    user_db = session.exec(
        select(User).where(
            or_(User.username == user.identifier, User.email == user.identifier)
        )
    ).one()

    if not user_db:
        return

    # Checking if password matchs with db
    if password_hash.verify(password=user.password, hash=user_db.hashed_password):
        payload = {
            "user_id": user_db.id,
            "exp": format_to_datetime(type="MINUTE", exp=settings.TOKEN_EXP_MINUTE),
        }

        # Creating token
        return jwt.encode(
            payload=payload, algorithm=settings.TOKEN_ALGORITHM, key=settings.TOKEN_KEY
        )
