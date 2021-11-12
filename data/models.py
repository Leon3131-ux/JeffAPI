from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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
    question_ratings = relationship("QuestionRating", cascade='all,delete')


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    question = Column(String(255), nullable=False)
    question_ratings = relationship("QuestionRating", cascade='all,delete')


class QuestionRating(Base):
    __tablename__ = "question_rating"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="question_ratings")
    question_id = Column(Integer, ForeignKey("question.id", ondelete='CASCADE'), nullable=False)
    question = relationship("Question", back_populates="question_ratings")
    rating = Column(Integer, nullable=False)


class QuestionLog(Base):
    __tablename__ = "question_log"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    question_id = Column(Integer, nullable=False)
    question = Column(String(255), nullable=False)
    method = Column(String(255), nullable=False)


class UserLog(Base):
    __tablename__ = "user_log"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    username = Column(String(255), nullable=False)
    method = Column(String(255), nullable=False)


class AuthModel(BaseModel):
    username: str
    password: str


class QuestionRatingOut(BaseModel):
    question_id: int
    question: str
    user_id: int
    rating: int

    class Config:
        orm_mode = True


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


class QuestionRatingIn(BaseModel):
    question_id: int
    rating: int
