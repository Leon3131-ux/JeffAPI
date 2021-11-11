from fastapi import APIRouter, Depends

from data.models import User, UserDto
from errorresponses.error_responses import forbidden_exception
from security.auth_handler import get_current_user, encrypt_password
from data.database import session

router = APIRouter()


@router.post("/api/user/create")
async def create_user(user_dto: UserDto, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:

        session.add(User(
            user_dto.username,
            encrypt_password(user_dto.password),
            user_dto.isAdmin
        ))
        session.commit()
    else:
        raise forbidden_exception


@router.post("/api/user/update")
async def save_user(user_dto: UserDto, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        matching_user = session.query(User).filter(User.username == user_dto.username).first()
        if matching_user is not None:
            matching_user.username = user_dto.username
            matching_user.password = user_dto.password
            matching_user.is_admin = user_dto.isAdmin
            session.commit()
    else:
        raise forbidden_exception
