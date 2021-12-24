__submodules__ = ["routes"]

from app.api.v1.utils import routes

from app.api.v1.utils.routes import (
    router,
)

__all__ = ["router", "routes"]
