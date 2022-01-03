from functools import lru_cache
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from pydantic.fields import Field


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = Field(
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

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    @classmethod
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins


@lru_cache()
def get_settings() -> Settings:
    return Settings()
