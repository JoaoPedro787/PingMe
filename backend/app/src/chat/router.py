from fastapi import Depends
from fastapi.routing import APIRouter
from typing import Annotated, Optional
from auth.dependencies import get_current_user
from database import SessionDep
from .models import Chat
from .schemas import (
    ChatUserIndividual,
    ChatUserGlobal,
    MessagePagination,
    ChatUserCreate,
)
from .exceptions import ChatNotFound
from . import services

router = APIRouter()


# GET METHOD


@router.get("/user", response_model=list[ChatUserGlobal])
def get_user_all_chats(
    current_user: Annotated[int, Depends(get_current_user)], session: SessionDep
):
    """
    ## Handles all chats from user
    - Uses authentication to get current_user (token)

    ## Response
    - All chats
    - Empty array if not chats
    """

    chats = services.get_user_all_chats(current_user, session)

    return [
        ChatUserGlobal.model_validate(
            chat_user,
            update={"other_participant": user},
        )
        for chat_user, user in chats
    ]


@router.get("/{chat_id}", response_model=ChatUserIndividual)
def get_chat(
    chat_id: int,
    current_user: Annotated[int, Depends(get_current_user)],
    session: SessionDep,
):
    """
    ## Handles chat from query (chat_id)
    - Uses authentication to get current_user (token)

    ## Response
    - Returns chatuser (individual user from chat)
    - Raises ChatNotFound
    """

    chat = services.get_chat(chat_id, current_user, session)

    if not chat:
        raise ChatNotFound()

    chatUser, user = chat

    return ChatUserIndividual.model_validate(
        chatUser,
        update={"other_participant": user},
    )


@router.get("/{chat_id}/messages", response_model=MessagePagination)
def get_chat_messages(
    chat_id,
    session: SessionDep,
    cursor: Optional[int] = None,
):
    """
    ## Get messages from chat based on query (chat_id)
    - Uses cursor pagination to get messages (high perfomance)

    ## Response
    - Returns messages
    - Don't return items if messages are not found
    """

    messages = services.get_chat_messages(chat_id, cursor, session)

    return messages


# POST METHOD


@router.post("", status_code=201, response_model=ChatUserIndividual)
def create_chat(
    current_user: Annotated[int, Depends(get_current_user)],
    session: SessionDep,
    other_user: ChatUserCreate,
):
    """
    o chat user pode ser deletado, porém o chat também? creio que não, pq as chaves não irão bater


    VERIFICA SE EXISTE E RETORNA O CHAT DA FORMA INDIVIDUAL

    AQUI SERIA O SEARCH PERSON
    DEVE SEMPRE RETORNAR UM CHAT
    """

    chat_id = services.verify_if_chat_exists(
        current_user, other_user.other_user_id, session
    )

    if not chat_id:
        chat_id = services.create_chat(current_user, other_user.other_user_id, session)

    chat = services.get_chat(chat_id, current_user, session, other_user.other_user_id)

    chatUser, user = chat

    return ChatUserIndividual.model_validate(
        chatUser,
        update={"other_participant": user},
    )
