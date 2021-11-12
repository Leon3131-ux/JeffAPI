from datetime import timedelta, datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from data.database import session as db
from data.models import User
from errorresponses.error_responses import authentication_exception, authorization_exception

SECRET_KEY = "veryCoolSecret"
EXPIRES_MINUTES = 60
ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(username: str, password: str):
    matching_user = db.query(User).filter(User.username == username).first()
    if matching_user is not None:
        password_matches = password_context.verify(password, matching_user.password)
        if password_matches:
            data = {
                "isAdmin": matching_user.is_admin,
                "sub": matching_user.username,
                "exp": datetime.utcnow() + timedelta(minutes=EXPIRES_MINUTES)
            }
            jwt_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
            return jwt_token
    raise authentication_exception


async def get_current_user(jwt_token: str = Depends(oauth2_scheme)):
    decoded_jwt_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
    username = decoded_jwt_token.get("sub")
    matching_user = db.query(User).filter(User.username == username).first()
    if matching_user is None:
        raise authorization_exception
    return matching_user



def encrypt_password(password: str):
    return password_context.hash(password)
