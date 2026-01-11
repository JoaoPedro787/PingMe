from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(unique=True, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    hashed_password: str
    profile_image: str
    joined_in: datetime = Field(default_factory=datetime.utcnow)
    disabled: bool = Field(default=False)
