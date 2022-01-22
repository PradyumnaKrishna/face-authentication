from fastapi import Depends, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlmodel import Session

from .db import get_session
from .exceptions import PermissionDenied
from .face_api import FaceAPI
from .models import User
from .settings import get_settings
from .token import verify_token
from .utils import get_user

settings = get_settings()
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.OAUTH_AUTH_URL, tokenUrl=settings.OAUTH_TOKEN_URL
)


def authenticate_user(user: User, file_url: str) -> User:
    face_api = FaceAPI()
    face_id = face_api.detect(file_url)
    if user.person_id and face_api.verify(user.person_id, face_id):
        return user
    raise PermissionDenied("Authentication Failed")


async def get_current_user(
    token: str = Security(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    credentials_exception = PermissionDenied("Could not validate credentials")
    token_data = verify_token(token, credentials_exception)
    user = get_user(username=token_data.username, session=session)
    if user:
        return user
    raise credentials_exception


__all__ = [
    "authenticate_user",
    "get_current_user",
]
