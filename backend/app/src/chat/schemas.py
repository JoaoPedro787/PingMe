from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from enum import StrEnum


class ChatUserIndividual(SQLModel):
    chat_id: int
    other_participant: "UserPublic"


class ChatUserGlobal(SQLModel):
    chat_id: int
    unread_messages: int
    last_message: Optional["MessagePublic"] = None
    other_participant: "UserPublic"


class MessagePagination(SQLModel):
    items: list[Optional["MessagePublic"]] = []
    next_cursor: Optional[int] = None
    has_more: bool


class ChatUserCreate(SQLModel):
    other_user_id: int


class MessageType(StrEnum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"


class MessagePublic(SQLModel):
    id: int
    user_id: int
    content: str
    type: "MessageType"
    created_at: datetime


from auth.schemas import UserPublic
