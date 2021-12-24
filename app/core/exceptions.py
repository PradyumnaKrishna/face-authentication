from typing import Any, Dict, Optional

from fastapi import HTTPException, status

from .utils import logger


class BadRequest(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        logger.info(detail)
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers
        )


class PermissionDenied(HTTPException):
    def __init__(self, detail: Any = None) -> None:
        logger.warning(detail)
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InternalError(HTTPException):
    def __init__(
        self, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        logger.error(detail)
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server Error",
            headers=headers,
        )
