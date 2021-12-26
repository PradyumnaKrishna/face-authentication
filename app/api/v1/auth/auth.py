from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    UploadFile,
)
from sqlmodel import Session

from app.core import authenticate_user, create_access_token, get_session
from app.core.exceptions import PermissionDenied
from app.core.utils import get_user, save_file
from ..tags import AUTH

router = APIRouter()


@router.post("/authorize", tags=[AUTH])
def authorize(
    request: Request,
    username: str = Form(...),
    image: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    base_url = request.base_url
    user = get_user(username, session)
    if not user:
        raise PermissionDenied("Invalid username")

    path = save_file(image)
    url = f"{base_url}{path}"

    user = authenticate_user(user=user, file_url=url)
    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", tags=[AUTH])
async def token(code: str = Form(...)):
    return {"access_token": code}
