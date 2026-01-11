from sqlmodel import SQLModel
from enum import StrEnum


class ChatPublic(SQLModel):
    id: int
    participants: list["ChatUserPublic"]
    messages: list["MessagePublic"]


class ChatUserPublic(SQLModel):
    id: int
    user_id: int


class MessageType(StrEnum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"


class MessagePublic(SQLModel):
    id: int
    user_id: int
    content: str
    type: MessageType
