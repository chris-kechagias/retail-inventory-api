"""
Variant routes: API endpoints for managing product variants.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, status

from ..controllers import (
    create_product_variant_controller,
    delete_product_variant_controller,
    get_product_controller,
    get_product_variants_controller,
    update_product_variant_controller,
)
from ..core import SessionDep
from ..core.errors import (
    ProductNotFoundException,
    ProductVariantNotFoundException,
)
from ..models import (
    ProductVariant,
    ProductVariantCreate,
    ProductVariantUpdate,
)

router = APIRouter(prefix="/products", tags=["Variants"])
logger = logging.getLogger(__name__)

# ----------------------------------------------------
# 1. READ ROUTES
# ----------------------------------------------------


@router.get(
    "/{product_id}/variants",
    response_model=list[ProductVariant],
    summary="Get all variants for a product",
)
def get_product_variants_router(
    product_id: UUID,
    session: SessionDep,
) -> list[ProductVariant]:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return get_product_variants_controller(product_id, session)


# ----------------------------------------------------
# 2. WRITE ROUTES (POST/PATCH/DELETE)
# ----------------------------------------------------


@router.post(
    "/{product_id}/variants",
    response_model=ProductVariant,
    status_code=status.HTTP_201_CREATED,
    summary="Add variants for an existing product",
)
def create_product_variant_router(
    product_id: UUID, variant: ProductVariantCreate, session: SessionDep
) -> ProductVariant:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    return create_product_variant_controller(product_id, variant, session)


@router.patch(
    "/{product_id}/variants/{variant_id}",
    response_model=ProductVariant,
    summary="Partial update of a product's variants",
)
def update_product_variant_router(
    product_id: UUID,
    variant_id: UUID,
    update_data: ProductVariantUpdate,
    session: SessionDep,
) -> ProductVariant:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    variant = update_product_variant_controller(variant_id, update_data, session)
    if not variant:
        raise ProductVariantNotFoundException(variant_id)
    return variant


@router.delete(
    "/{product_id}/variants/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a product's variants",
)
def delete_product_variant_router(
    product_id: UUID,
    variant_id: UUID,
    session: SessionDep,
) -> None:
    product = get_product_controller(product_id, session)
    if not product:
        raise ProductNotFoundException(product_id)
    variant = delete_product_variant_controller(variant_id, session)
    if not variant:
        raise ProductVariantNotFoundException(variant_id)
