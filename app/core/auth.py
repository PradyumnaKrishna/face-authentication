from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from pydantic.networks import AnyHttpUrl
from sqlmodel import Session

from .db import get_session
from .exceptions import PermissionDenied
from .face_api import FaceAPI
from .models import TokenData, User
from .settings import get_settings
from .utils import get_user

settings = get_settings()
SECRET_KEY = settings.AUTH_SECRET_KEY
ALGORITHM = settings.AUTH_ALGORITHM
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.OAUTH_AUTH_URL, tokenUrl=settings.OAUTH_TOKEN_URL
)


def authenticate_user(user: User, file_url: AnyHttpUrl) -> Optional[User]:
    face_api = FaceAPI()
    face_id = face_api.detect(file_url)
    if not face_api.verify(user.person_id, face_id):
        raise PermissionDenied("Authentication Failed")

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=AUTH_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Security(oauth2_scheme), session: Session = Depends(get_session)
) -> Optional[User]:
    credentials_exception = PermissionDenied("Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as error:
        raise credentials_exception from error

    user = get_user(username=token_data.username, session=session)
    if user is None:
        raise credentials_exception
    return user


__all__ = [
    "authenticate_user",
    "create_access_token",
    "get_current_user",
]
