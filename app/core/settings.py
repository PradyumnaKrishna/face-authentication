from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseSettings
from pydantic.fields import Field


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=[
            "http://localhost",
            "http://localhost:8080",
            "https://localhost",
        ]
    )
    PROJECT_NAME: str = "face-authentication"
    SQLDB_URI: str = "sqlite:///sqlite3.db"

    FACE_API_ENDPOINT: str = ""
    FACE_API_KEY: str = ""
    FACE_API_GROUP: str = ""

    OAUTH_AUTH_URL: str = "/api/v1/authorize"
    OAUTH_TOKEN_URL: str = "/api/v1/token"

    AUTH_ALGORITHM: str = "HS256"
    AUTH_SECRET_KEY: str = "RkJ70sv0mp8ZqWcqyFNrZzZBt6piYQUSgQ9dQ7njxPryEiPb2XgLFOaw-0_khG40Fc7OgfvfzwB-C0R1V0WeIw"
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
