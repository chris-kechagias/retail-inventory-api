# Third-Party Imports
from fastapi import APIRouter

# Local/First-Party Imports
from config import config

router = APIRouter()


@router.get("/", tags=["System"])
def read_root():
    return {
        "message": config.app_name,
        "version": config.version,
        "docs": "/docs",
        "endpoints": "/products",
    }
