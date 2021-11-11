from fastapi import APIRouter, Depends
from typing import List

from data.models import User, UserDto
from errorresponses.error_responses import forbidden_exception, bad_request
from security.auth_handler import get_current_user, encrypt_password
from data.database import session as db

router = APIRouter()


@router.get("/api/user/get", response_model=List[UserDto], response_model_exclude={"password"})
async def get_users(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        users = db.query(User).all()
        return users
    else:
        raise forbidden_exception


@router.post("/api/user/save", response_model=UserDto, response_model_exclude={"password"})
async def save_user(user_dto: UserDto, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        user = db.query(User).filter(User.id == user_dto.id).first()
        if user is not None:
            user.username = user_dto.username
            user.password = user_dto.password
            user.is_admin = user_dto.is_admin
        else:
            user_with_same_name = db.query(User).filter(User.id == user_dto.id).first()
            if user_with_same_name is None:
                user = User(username=user_dto.username, password=user_dto.password, is_admin=user_dto.is_admin)
                db.add(user)
                db.flush()
            else:
                raise bad_request
        db.commit()
        return user
    else:
        raise forbidden_exception


@router.delete("/api/user/delete/{user_id}")
async def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        matching_user = db.query(User).filter(User.id == user_id).first()
        if matching_user is not None:
            db.delete(matching_user)
            db.commit()
    else:
        raise forbidden_exception
