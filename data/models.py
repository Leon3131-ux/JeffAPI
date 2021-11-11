from sqlalchemy import Column, Integer, String, Boolean

from data.database import Base
from pydantic import BaseModel


class User(Base):
    def __init__(self, username: str, password: str, is_admin: bool):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean(255), nullable=False, name="is_admin")


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    question = Column(String(255), nullable=False)


class AuthModel(BaseModel):
    username: str
    password: str


class UserDto(BaseModel):
    id: int
    username: str
    password: str
    is_admin: bool

    class Config:
        orm_mode = True


class QuestionDto(BaseModel):
    id: int
    question: str

    class Config:
        orm_mode = True
