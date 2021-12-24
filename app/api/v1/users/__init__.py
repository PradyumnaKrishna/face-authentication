__submodules__ = ["routes"]

from app.api.v1.users import routes

from app.api.v1.users.routes import (
    router,
)

__all__ = ["router", "routes"]
