"""
This module defines the API routes for managing products and their variants in the retail inventory system. It includes endpoints for creating, reading, updating, and deleting products and variants, as well as an analytics endpoint to calculate the total inventory value."""

# Standard Library Imports
import logging
from typing import Annotated

# Third-Party Imports
from fastapi import APIRouter, Query, status

# Local/First-Party Imports
from database import SessionDep
from exceptions import ProductNotFoundException, ProductVariantNotFoundException
from models import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductVariant,
    ProductVariantCreate,
    ProductVariantUpdate,
)
from services import (
    create_product_controller,
    create_product_variant_controller,
    delete_product_controller,
    delete_product_variant_controller,
    get_all_products_controller,
    get_inventory_value_controller,
    get_product_controller,
    get_product_variants_controller,
    update_product_controller,
    update_product_variant_controller,
)

router = APIRouter()
logger = logging.getLogger(__name__)

# ----------------------------------------------------
# 1. ANALYTICS ROUTES
# ----------------------------------------------------


@router.get(
    "/products/total_value",
    summary="Calculate the total monetary value of the current inventory",
    response_model=dict[str, float],
)
def get_inventory_value_router(session: SessionDep):
    return get_inventory_value_controller(session)


# ----------------------------------------------------
# 2. READ ROUTES
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


@router.get(
    "/products/{product_id}/variants",
    response_model=list[ProductVariant],
    summary="Get all variants for a product",
)
def get_product_variants_router(
    product_id: int,
    session: SessionDep,
) -> list[ProductVariant]:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return get_product_variants_controller(product_id, session)


# ----------------------------------------------------
# 3. WRITE ROUTES (POST/PATCH/DELETE)
# ----------------------------------------------------


@router.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new product to the inventory",
)
def create_product_router(product: ProductCreate, session: SessionDep) -> Product:
    return create_product_controller(product, session)


@router.post(
    "/products/{product_id}/variants",
    response_model=ProductVariant,
    status_code=status.HTTP_201_CREATED,
    summary="Add variants for an existing product",
)
def create_product_variant_router(
    product_id: int, variant: ProductVariantCreate, session: SessionDep
) -> ProductVariant:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return create_product_variant_controller(product_id, variant, session)


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


@router.patch(
    "/products/{product_id}/variants/{variant_id}",
    response_model=ProductVariant,
    summary="Partial update of a product's variants",
)
def update_product_variant_router(
    product_id: int,
    variant_id: int,
    update_data: ProductVariantUpdate,
    session: SessionDep,
) -> ProductVariant:
    variant = update_product_variant_controller(variant_id, update_data, session)
    if not variant:
        raise ProductVariantNotFoundException(variant_id)
    return variant


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


@router.delete(
    "/products/{product_id}/variants/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a product's variants",
)
def delete_product_variant_router(
    product_id: int,
    variant_id: int,
    session: SessionDep,
) -> None:
    variant = delete_product_variant_controller(variant_id, session)
    if not variant:
        raise ProductVariantNotFoundException(variant_id)
