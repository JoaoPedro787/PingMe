from fastapi import Depends
from fastapi.routing import APIRouter
from typing import Annotated, Optional
from auth.dependencies import get_current_user
from database import SessionDep
from .models import Chat
from .schemas import ChatUserIndividual, ChatUserGlobal, MessagePagination
from .exceptions import ChatNotFound
from . import services

router = APIRouter()


@router.get("/user")
def get_user_all_chats(
    user: Annotated[int, Depends(get_current_user)], session: SessionDep
):

    chats = services.get_user_all_chats(user, session)

    if not chats:
        raise ChatNotFound()

    return [
        ChatUserGlobal.model_validate(
            chat_user,
            update={"other_participant": user},
        )
        for chat_user, user in chats
    ]


@router.get("/{id}", response_model=ChatUserIndividual)
def get_chat(
    id: int, user: Annotated[int, Depends(get_current_user)], session: SessionDep
):

    chat = services.get_chat(id, user, session)

    if not chat:
        raise ChatNotFound()

    chatUser, user = chat

    return ChatUserIndividual.model_validate(
        chatUser,
        update={"other_participant": user},
    )


@router.get("/{id}/messages", response_model=MessagePagination)
def get_chat_messages(
    id,
    session: SessionDep,
    cursor: Optional[int] = None,
):
    messages = services.get_chat_messages(id, cursor, session)

    return messages
