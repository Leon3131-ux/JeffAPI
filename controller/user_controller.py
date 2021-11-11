from fastapi import APIRouter, Depends

from data.models import User, NewUserModel
from security.auth_handler import get_current_user, encrypt_password
from security.auth_handler import forbidden_exception
from data.database import session

router = APIRouter()


@router.post("/api/user/create")
async def create_user(new_user: NewUserModel, current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        session.add(User(
            new_user.username,
            encrypt_password(new_user.password),
            new_user.isAdmin
        ))
        session.commit()
    else:
        raise forbidden_exception
