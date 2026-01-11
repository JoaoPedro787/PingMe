from pwdlib import PasswordHash
from sqlmodel import select, or_
from .models import User
from .schemas import Token
from config import settings
from datetime import datetime, timedelta, timezone
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
        exp_date = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.TOKEN_EXP_MINUTE
        )

        payload = Token(user_id=user_db.id, exp=exp_date).model_dump()

        # Creating token
        return {
            "encoded": jwt.encode(
                payload=payload,
                algorithm=settings.TOKEN_ALGORITHM,
                key=settings.TOKEN_KEY,
            ),
            "expire_date": exp_date,
        }
