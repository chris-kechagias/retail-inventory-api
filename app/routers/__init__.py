from .analytics import router as analytics_router
from .health import router as health_router
from .home import router as home_router
from .products import router as products_router
from .variants import router as variants_router

__all__ = [
    "analytics_router",
    "health_router",
    "home_router",
    "products_router",
    "variants_router",
]
