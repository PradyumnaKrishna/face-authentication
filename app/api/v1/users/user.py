from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Request,
    UploadFile,
)
from sqlmodel import Session

from app.core import FaceAPI, get_current_user, get_session
from app.core.exceptions import BadRequest
from app.core.models import UserRead, User
from app.core.utils import get_user, save_file
from ..tags import USER

router = APIRouter()
face_api = FaceAPI()


@router.post("/", response_model=UserRead, tags=[USER])
def create_user(
    request: Request,
    username: str = Form(...),
    secret: str = Form(...),
    image: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    base_url = request.base_url
    user = get_user(username, session)
    if user:
        raise BadRequest("User Already Exist")

    person_id = face_api.create_person(name=username)

    path = save_file(image)
    url = f"{base_url}{path}"

    face_api.add_face(person_id, url)

    db_user = User(username=username, secret=secret)
    db_user.person_id = person_id

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/me", response_model=UserRead, tags=[USER])
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{username}", tags=[USER])
async def check(username: str, session: Session = Depends(get_session)):
    if get_user(username, session):
        return True
    return False


@router.post("/upload", tags=[USER])
def upload(
    request: Request,
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    base_url = request.base_url
    path = save_file(image)

    url = f"{base_url}{path}"
    if current_user.person_id:
        face_api.add_face(current_user.person_id, url)
        return "success"

    return BadRequest(f"user `{current_user.username}` doesn't have a `person_id`")
