from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(SQLModel):
    username: str
    email: EmailStr
    profile_image: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    identifier: str
    password: str


class UserUpdate(UserBase):
    disabled: bool


class UserPublic(SQLModel):
    id: int
    username: str
    profile_image: str
    disabled: bool
    joined_in: datetime
