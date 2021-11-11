from fastapi import APIRouter

from data.models import AuthModel
from security.auth_handler import create_token

router = APIRouter()


@router.post("/token")
async def login(auth_model: AuthModel):
    token = create_token(auth_model.username, auth_model.password)
    return {"access_token": token, "token_type": "bearer"}

