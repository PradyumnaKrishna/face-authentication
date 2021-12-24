from fastapi import APIRouter

from . import auth
from . import users
from . import utils


def get_routes() -> APIRouter:
    api_router = APIRouter()

    api_router.include_router(auth.router)
    api_router.include_router(users.router)
    api_router.include_router(utils.router)

    return api_router
