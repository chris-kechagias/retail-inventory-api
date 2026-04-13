"""
Product routes: API endpoints for creating, reading, updating and deleting products.
"""

import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from ..controllers import (
    create_product_controller,
    delete_product_controller,
    get_all_products_controller,
    get_product_controller,
    get_searchable_products_controller,
    update_product_controller,
)
from ..core import SessionDep
from ..core.errors import ProductNotFoundException
from ..models import (
    Product,
    ProductCreate,
    ProductUpdate,
)

router = APIRouter(prefix="/products", tags=["Products"])
logger = logging.getLogger(__name__)


# ----------------------------------------------------
# 1. READ ROUTES
# ----------------------------------------------------


@router.get(
    "/",
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
    "/search",
    response_model=list[Product],
    summary="Search products by name or SKU",
)
def get_searchable_products_router(q: str, session: SessionDep):
    return get_searchable_products_controller(q, session)


@router.get(
    "/{product_id}",
    response_model=Product,
    summary="Get product by ID",
)
def get_product_router(product_id: UUID, session: SessionDep) -> Product:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return product


# ----------------------------------------------------
# 2. WRITE ROUTES (POST/PATCH/DELETE)
# ----------------------------------------------------


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new product to the inventory",
)
def create_product_router(product: ProductCreate, session: SessionDep) -> Product:
    return create_product_controller(product, session)


@router.patch(
    "/{product_id}",
    response_model=Product,
    summary="Partial update of a product",
)
def update_product_router(
    product_id: UUID, update_data: ProductUpdate, session: SessionDep
) -> Product:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return update_product_controller(product_id, update_data, session)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a product",
)
def delete_product_router(product_id: UUID, session: SessionDep) -> None:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    delete_product_controller(product_id, session)
