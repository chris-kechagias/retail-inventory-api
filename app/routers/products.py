"""
Docstring for app.routers.products
"""
# Standard Library Imports
import logging
from typing import Annotated, Dict, List

# Third-Party Imports
from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import func, select

# Local/First-Party Imports
from app.database import SessionDep
from app.models import Product, ProductCreate, ProductUpdate

router = APIRouter()
logger = logging.getLogger(__name__)

# ----------------------------------------------------
# 1. ANALYTICS ROUTES
# ----------------------------------------------------


@router.get(
    "/products/total_value",
    summary="Calculate the total monetary value of the current inventory",
    response_model=Dict[str, float],
)
def get_inventory_value(session: SessionDep):
    """
    Calculates the aggregate value (price * quantity) of all inventory.

    Utilizes SQL-side aggregation (func.sum) to ensure high performance
    even with thousands of rows, avoiding Python-level loops.
    """
    logger.info("Executing database-side aggregation for total inventory value.")

    # Calculate (price * quantity) per row and sum them up in the DB engine
    statement = select(func.sum(Product.price * Product.quantity))
    result = session.exec(statement).one()
    total_value = result or 0.0

    logger.info("Total inventory value successfully calculated", extra={"total_value": total_value})

    return {"Total Inventory Value $": total_value}


