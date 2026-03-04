"""
This module contains the core business logic
for managing products and their variants in the inventory system.
Each function corresponds to a specific operation (CRUD) on the Product
and ProductVariant models, and interacts with the database via SQLModel sessions.
"""

# Standard Library Imports
import logging
from typing import Optional

# Third-Party Imports
from sqlmodel import func, select

# Local/First-Party Imports
from database import SessionDep
from models import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductVariant,
    ProductVariantCreate,
    ProductVariantUpdate,
)

logger = logging.getLogger(__name__)


def get_inventory_value_controller(session: SessionDep):
    """
    Calculates the aggregate value (price * quantity) of all inventory.

    Utilizes SQL-side aggregation (func.sum) to ensure high performance
    even with thousands of rows, avoiding Python-level loops.
    """

    logger.info("Executing database-side aggregation for total inventory value.")

    # Calculate (price * quantity) per row and sum them up in the DB engine
    statement = select(func.sum(Product.price * ProductVariant.quantity)).join(
        ProductVariant, Product.id == ProductVariant.product_id
    )
    result = session.exec(statement).one()
    total_value = result or 0.0

    logger.info(
        "Total inventory value successfully calculated",
        extra={"total_value": total_value},
    )

    return {"Total Inventory Value $": total_value}


def get_all_products_controller(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
):
    """
    Retrieves a list of products using offset/limit pagination.

    Args:
        offset: The number of items to skip.
        limit: The maximum number of items to return (capped at 100).
    """
    statement = select(Product).offset(offset).limit(limit)
    products = session.exec(statement).all()
    logger.info("Products retrieved successfully", extra={"count": len(products)})
    return products


def get_product_controller(product_id: int, session: SessionDep) -> Optional[Product]:
    """
    Fetches a single product record.
    """
    logger.info("Attempting to fetch product", extra={"product_id": product_id})
    product = session.get(Product, product_id)
    if product:
        logger.info("Product fetched successfully", extra={"product_id": product_id})
    return product


def get_product_variants_controller(
    product_id: int, session: SessionDep
) -> list[ProductVariant]:
    """
    Fetches the variants of the selected product.
    """
    logger.info(
        "Attempting to fetch product variants", extra={"product_id": product_id}
    )
    statement = select(ProductVariant).where(ProductVariant.product_id == product_id)
    variants = session.exec(statement).all()
    logger.info(
        "Product variants fetched successfully",
        extra={"product_id": product_id, "count": len(variants)},
    )
    return variants


def create_product_controller(product: ProductCreate, session: SessionDep) -> Product:
    """
    Persists a new product record.

    Validates input using ProductCreate and maps it to the Product table model.
    The database automatically handles ID generation and stock-status logic.
    """

    logger.info(
        "Creating new product",
        extra={
            "category": product.category,
            "name": product.name,
            "color": product.color,
            "price": product.price,
            "collection": product.collection,
            "coming_soon": product.coming_soon,
        },
    )
    # 1. Converts the Pydantic schema into a SQLModel Table instance
    db_product = Product.model_validate(product)
    # 2. Add to session and commit to persist
    session.add(db_product)
    session.commit()
    session.refresh(db_product)  # Syncs db_product with the DB-generated ID

    logger.info("Product created successfully", extra={"product_id": db_product.id})

    return db_product


def create_product_variant_controller(
    product_id: int, variant: ProductVariantCreate, session: SessionDep
) -> ProductVariant:
    """
    Persists a new variant for the given product.

    Links the variant to its parent product via product_id
    and delegates ID generation to PostgreSQL.
    """

    logger.info(
        "Creating product variant",
        extra={
            "product_id": product_id,
            "size": variant.size,
            "quantity": variant.quantity,
            "in_stock": variant.in_stock,
        },
    )

    # 1. Converts the Pydantic schema into a SQLModel Table instance
    db_variant = ProductVariant.model_validate(variant)
    db_variant.product_id = product_id
    # 2. Add to session and commit to persist
    session.add(db_variant)
    session.commit()
    session.refresh(db_variant)  # Syncs db_variant with the DB-generated ID

    logger.info(
        "Product variant created successfully",
        extra={"variant_id": db_variant.id, "product_id": product_id},
    )

    return db_variant


def update_product_controller(
    product_id: int, update_data: ProductUpdate, session: SessionDep
) -> Product:
    """
    Updates specific fields of an existing product.

    Uses 'exclude_unset=True' to ensure only fields provided in the
    request body are modified, preserving other existing values.
    """

    logger.info(
        "Updating product",
        extra={
            "product_id": product_id,
            "category": update_data.category,
            "name": update_data.name,
            "color": update_data.color,
            "price": update_data.price,
            "collection": update_data.collection,
            "coming_soon": update_data.coming_soon,
        },
    )

    db_product = session.get(Product, product_id)
    # Return None if there is no product
    if not db_product:
        logger.warning("Product not found", extra={"product_id": product_id})
        return None

    # Update only the fields provided in update_data
    product_data = update_data.model_dump(exclude_unset=True)

    # Update the database product with the new data
    for key, value in product_data.items():
        setattr(db_product, key, value)

    # Add to session and commit to persist
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    logger.info(
        "Product updated successfully",
        extra={
            "product_id": product_id,
            "category": db_product.category,
            "name": db_product.name,
            "color": db_product.color,
            "price": db_product.price,
            "collection": db_product.collection,
            "coming_soon": db_product.coming_soon,
        },
    )

    return db_product


def update_product_variant_controller(
    variant_id: int, update_data: ProductVariantUpdate, session: SessionDep
) -> ProductVariant:
    """
    Updates a product variant by its ID.
    Applies only the fields provided in the request body.
    Returns the updated variant, or None if not found.
    """

    logger.info(
        "Updating product variant",
        extra={
            "variant_id": variant_id,
            "size": update_data.size,
            "quantity": update_data.quantity,
            "in_stock": update_data.in_stock,
        },
    )

    db_variant = session.get(ProductVariant, variant_id)
    # Return None if there is no variant
    if not db_variant:
        logger.warning("Product variant not found", extra={"variant_id": variant_id})
        return None

    # Update only the fields provided in update_data
    variant_data = update_data.model_dump(exclude_unset=True)

    # Update the database product with the new data
    for key, value in variant_data.items():
        setattr(db_variant, key, value)

    # Add to session and commit to persist
    session.add(db_variant)
    session.commit()
    session.refresh(db_variant)

    logger.info(
        "Product variant updated successfully",
        extra={
            "variant_id": variant_id,
            "size": db_variant.size,
            "quantity": db_variant.quantity,
            "in_stock": db_variant.in_stock,
        },
    )

    return db_variant


def delete_product_controller(
    product_id: int, session: SessionDep
) -> Optional[Product]:
    """
    Deletes a product from the database.
    """
    logger.info("Attempting to delete product", extra={"product_id": product_id})
    db_product = session.get(Product, product_id)

    if not db_product:
        return None

    session.delete(db_product)
    session.commit()

    logger.info("Product deleted successfully", extra={"product_id": product_id})

    return db_product


def delete_product_variant_controller(
    variant_id: int, session: SessionDep
) -> Optional[ProductVariant]:
    """
    Deletes the variants of a product from the database.
    """
    logger.info(
        "Attempting to delete product variant", extra={"variant_id": variant_id}
    )
    db_variant = session.get(ProductVariant, variant_id)

    if not db_variant:
        return None

    session.delete(db_variant)
    session.commit()

    logger.info(
        "Product variant deleted successfully", extra={"variant_id": variant_id}
    )

    return db_variant
