from sqlalchemy import Column, Integer, String, Boolean

from data.database import Base
from pydantic import BaseModel


class User(Base):
    def __init__(self, username: str, password: str, is_admin: bool):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, name="is_admin")


class AuthModel(BaseModel):
    username: str
    password: str


class NewUserModel(BaseModel):
    username: str
    password: str
    isAdmin: bool
