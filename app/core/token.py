from datetime import datetime, timedelta

from jose import JWTError, jwt

from .models import TokenData
from .settings import get_settings

settings = get_settings()
SECRET_KEY = settings.AUTH_SECRET_KEY
ALGORITHM = settings.AUTH_ALGORITHM
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError as error:
        raise credentials_exception from error


__all__ = [
    "create_access_token",
    "verify_token",
]
