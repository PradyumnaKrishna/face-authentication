import uuid
from logging import getLogger
from typing import Optional

from fastapi import UploadFile
from sqlmodel import select, Session

from .models import User

logger = getLogger("uvicorn.error")


def get_user(username: str, session: Session) -> Optional[User]:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if user:
        return user
    return None


def save_file(file: UploadFile) -> str:
    filename = uuid.uuid4()
    path = f"static/{filename}"
    with open(path, "wb") as f:
        content = file.file.read()
        f.write(content)

    return path
