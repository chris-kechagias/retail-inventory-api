"""
Health routes: API endpoints for health checks and system status.
"""

import time

from fastapi import APIRouter

from ..core import config
from ..models import HealthResponse

router = APIRouter(tags=["System"])


@router.head("/health")
@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok", version=config.version, uptime=time.time() - config.start_time
    )
