"""
Home route: API endpoint for the root path, providing basic information about the API.
"""

from fastapi import APIRouter

from ..core import config

router = APIRouter(tags=["System"])


@router.get("/")
def read_root():
    return {
        "message": config.app_name,
        "version": config.version,
        "docs": "/docs",
        "endpoints": "/products",
    }
