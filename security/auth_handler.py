from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from data.database import session as db
from data.models import User

SECRET_KEY = "veryCoolSecret"
EXPIRES_MINUTES = 60
ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

authorization_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could Not Validate Token",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could Not Validate Token",
    headers={"WWW-Authenticate": "Bearer"},
)

authentication_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

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
    try:
        decoded_jwt_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_jwt_token.get("sub")
        matching_user = db.query(User).filter(User.username == username).first()
        if matching_user is None:
            raise authorization_exception
        return matching_user
    except JWTError:
        raise authorization_exception


def encrypt_password(password: str):
    return password_context.hash(password)
