"""
Product routes: API endpoints for creating, reading, updating and deleting products.
"""

# Standard Library Imports
import logging
from typing import Annotated

# Third-Party Imports
from fastapi import APIRouter, Query, status

from ..controllers.products import (
    create_product_controller,
    delete_product_controller,
    get_all_products_controller,
    get_product_controller,
    update_product_controller,
)

# Local/First-Party Imports
from ..database import SessionDep
from ..models import (
    Product,
    ProductCreate,
    ProductUpdate,
)
from ..utils.errors import ProductNotFoundException

router = APIRouter(tags=["Products"])
logger = logging.getLogger(__name__)


# ----------------------------------------------------
# 1. READ ROUTES
# ----------------------------------------------------


@router.get(
    "/products",
    response_model=list[Product],
    summary="List all products with pagination",
)
def get_all_products_router(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return get_all_products_controller(session, offset, limit)


@router.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Get product by ID",
)
def get_product_router(product_id: int, session: SessionDep) -> Product:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return product


# ----------------------------------------------------
# 2. WRITE ROUTES (POST/PATCH/DELETE)
# ----------------------------------------------------


@router.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new product to the inventory",
)
def create_product_router(product: ProductCreate, session: SessionDep) -> Product:
    return create_product_controller(product, session)


@router.patch(
    "/products/{product_id}",
    response_model=Product,
    summary="Partial update of a product",
)
def update_product_router(
    product_id: int, update_data: ProductUpdate, session: SessionDep
) -> Product:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return update_product_controller(product_id, update_data, session)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a product",
)
def delete_product_router(product_id: int, session: SessionDep) -> None:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    delete_product_controller(product_id, session)
