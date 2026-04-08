"""
Analytics routes: API endpoints for inventory analytics and reporting.
"""

import logging

from fastapi import APIRouter

from ..controllers import get_inventory_value_controller
from ..core import SessionDep

router = APIRouter(tags=["Analytics"])
logger = logging.getLogger(__name__)

# ----------------------------------------------------
# ANALYTICS ROUTES
# ----------------------------------------------------


@router.get(
    "/products/total_value",
    summary="Calculate the total monetary value of the current inventory",
    response_model=dict[str, float],
)
def get_inventory_value_router(session: SessionDep):
    return get_inventory_value_controller(session)
