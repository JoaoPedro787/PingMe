from sqlmodel import SQLModel, Field, Relationship
from .schemas import MessageType


class Chat(SQLModel, table=True):
    id: int = Field(primary_key=True)
    participants: list["ChatUser"] = Relationship(back_populates="chat")
    messages: list["Message"] = Relationship(back_populates="chat")


class ChatUser(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    chat_id: int = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="participants")


class Message(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chat_id: int = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="messages")
    user_id: int = Field(foreign_key="user.id")
    content: str = Field(nullable=False)
    type: MessageType


from auth.models import User
