"""
Analytics routes: API endpoints for inventory analytics and reporting.
"""

# Standard Library Imports
import logging

# Third-Party Imports
from fastapi import APIRouter

from ..controllers import get_inventory_value_controller

# Local/First-Party Imports
from ..database import SessionDep

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
