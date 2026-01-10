from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr = Field(unique=True, nullable=False)
    profile_image: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    disabled: bool


class UserPublic(BaseModel):
    id: int
    username: str
    profile_image: str
    disabled: bool
    joined_in: datetime
