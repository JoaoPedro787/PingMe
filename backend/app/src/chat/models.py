from sqlmodel import SQLModel, Field, Relationship
from pydantic import computed_field
from typing import Optional
from datetime import datetime
from .schemas import MessageType


class Chat(SQLModel, table=True):
    id: int = Field(primary_key=True)
    participants: list["ChatUser"] = Relationship(back_populates="chat")
    messages: list["Message"] = Relationship(back_populates="chat")


class ChatUser(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    chat_id: int = Field(foreign_key="chat.id")
    unread_messages: int = Field(default=0)
    last_message_id: Optional[int] = Field(foreign_key="message.id", nullable=True)
    last_message: "Message" = Relationship()
    chat: "Chat" = Relationship(back_populates="participants")
    user: "User" = Relationship()


class Message(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chat_id: int = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="messages")
    user_id: int = Field(foreign_key="user.id")
    content: str = Field(nullable=False)
    type: MessageType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # mensagem lida


from auth.models import User
