from fastapi import APIRouter, File, Request, UploadFile

from app.core.utils import save_file
from ..tags import UTILS

router = APIRouter()


@router.post("/upload", tags=[UTILS])
def upload_file(*, file: UploadFile = File(...), request: Request):
    base_url = request.base_url
    path = save_file(file)

    return {"url": f"{base_url}{path}"}
