from fastapi.routing import APIRouter
from database import SessionDep
from sqlmodel import select
from sqlalchemy.orm import selectinload
from .models import Chat
from .schemas import ChatPublic

router = APIRouter()


@router.get("", response_model=ChatPublic)
def get_chat(session: SessionDep):
    chats = session.exec(
        select(Chat).options(
            selectinload(Chat.messages), selectinload(Chat.participants)
        )
    ).one()

    return chats
