from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from database import SessionDep
from models import (
    Product,
)
from services import (
    get_all_products,
    get_inventory_value,
    get_product
)

router = APIRouter()

# ----------------------------------------------------
# 1. ANALYTICS ROUTES
# ----------------------------------------------------


@router.get(
    "/products/total_value",
    summary="Calculate the total monetary value of the current inventory",
    response_model=dict[str, float],
)
def get_inventory_value_endpoint(session: SessionDep):
    return get_inventory_value(session)


# ----------------------------------------------------
# 2. READ ROUTES
# ----------------------------------------------------


@router.get(
    "/products",
    response_model=list[Product],
    summary="List all products with pagination",
)
def get_all_products_endpoint(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_all_products(session, offset, limit)


@router.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Get product by ID",
)
def get_product_endpoint(product_id: int, session: SessionDep) -> Product:
    product = get_product(product_id, session)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )
    return product
