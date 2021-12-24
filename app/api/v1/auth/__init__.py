__submodules__ = ["routes"]

from app.api.v1.auth import routes

from app.api.v1.auth.routes import (
    router,
)

__all__ = ["router", "routes"]
