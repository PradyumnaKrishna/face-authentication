from fastapi import APIRouter

from . import utils

router = APIRouter()
router.include_router(utils.router, prefix="/utils")
