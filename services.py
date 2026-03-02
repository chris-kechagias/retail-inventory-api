""" """

# Standard Library Imports
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


def get_inventory_value_controller(session: SessionDep):
    """
    Calculates the aggregate value (price * quantity) of all inventory.

    Utilizes SQL-side aggregation (func.sum) to ensure high performance
    even with thousands of rows, avoiding Python-level loops.
    """

    # Calculate (price * quantity) per row and sum them up in the DB engine
    statement = select(func.sum(Product.price * ProductVariant.quantity)).join(
        ProductVariant, Product.id == ProductVariant.product_id
    )
    result = session.exec(statement).one()
    total_value = result or 0.0

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
    return products


def get_product_controller(product_id: int, session: SessionDep) -> Optional[Product]:
    """
    Fetches a single product record.
    """
    product = session.get(Product, product_id)
    return product


def get_product_variants_controller(
    product_id: int, session: SessionDep
) -> list[ProductVariant]:
    """
    Fetches the variants of the selected product.
    """
    statement = select(ProductVariant).where(ProductVariant.product_id == product_id)
    variants = session.exec(statement).all()
    return variants


def create_product_controller(product: ProductCreate, session: SessionDep) -> Product:
    """
    Persists a new product record.

    Validates input using ProductCreate and maps it to the Product table model.
    The database automatically handles ID generation and stock-status logic.
    """

    # 1. Converts the Pydantic schema into a SQLModel Table instance
    db_product = Product.model_validate(product)
    # 2. Add to session and commit to persist
    session.add(db_product)
    session.commit()
    session.refresh(db_product)  # Syncs db_product with the DB-generated ID

    return db_product


def create_product_variant_controller(
    product_id: int, variant: ProductVariantCreate, session: SessionDep
) -> ProductVariant:
    """
    Persists a new variant for the given product.

    Links the variant to its parent product via product_id
    and delegates ID generation to PostgreSQL.
    """
    # 1. Converts the Pydantic schema into a SQLModel Table instance
    db_variant = ProductVariant.model_validate(variant)
    db_variant.product_id = product_id
    # 2. Add to session and commit to persist
    session.add(db_variant)
    session.commit()
    session.refresh(db_variant)  # Syncs db_variant with the DB-generated ID

    return db_variant


def update_product_controller(
    product_id: int, update_data: ProductUpdate, session: SessionDep
) -> Product:
    """
    Updates specific fields of an existing product.

    Uses 'exclude_unset=True' to ensure only fields provided in the
    request body are modified, preserving other existing values.
    """

    db_product = session.get(Product, product_id)
    # Return None if there is no product
    if not db_product:
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

    return db_product


def update_product_variant_controller(
    variant_id: int, update_data: ProductVariantUpdate, session: SessionDep
) -> ProductVariant:
    """
    Updates a product variant by its ID.
    Applies only the fields provided in the request body.
    Returns the updated variant, or None if not found.
    """
    db_variant = session.get(ProductVariant, variant_id)
    # Return None if there is no product
    if not db_variant:
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

    return db_variant


def delete_product_controller(
    product_id: int, session: SessionDep
) -> Optional[Product]:
    """
    Deletes a product from the database.
    """
    db_product = session.get(Product, product_id)

    if not db_product:
        return None

    session.delete(db_product)
    session.commit()

    return db_product


def delete_product_variant_controller(
    variant_id: int, session: SessionDep
) -> Optional[ProductVariant]:
    """
    Deletes the variants of a product from the database.
    """
    db_variant = session.get(ProductVariant, variant_id)

    if not db_variant:
        return None

    session.delete(db_variant)
    session.commit()

    return db_variant
