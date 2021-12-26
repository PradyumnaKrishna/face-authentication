from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


class UserBase(SQLModel):
    __table_args__ = (UniqueConstraint("username"),)
    username: str
    secret: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: Optional[str]


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
