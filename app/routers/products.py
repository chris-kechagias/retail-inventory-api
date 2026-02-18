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


# ----------------------------------------------------
# 2. READ ROUTES
# ----------------------------------------------------


@router.get(
    "/products",
    response_model=List[Product],
    summary="List all products with pagination",
)
def get_all_products(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
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


@router.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Get product by ID",
)
def get_product(product_id: int, session: SessionDep) -> Product:
    """
    Fetches a single product record. Raises 404 if the ID does not exist.
    """
    logger.info("Attempting to fetch product", extra={"product_id": product_id})
    product = session.get(Product, product_id)

    if not product:
        # Raise the standard HTTP 404 if not found
        logger.warning("Product not found", extra={"product_id": product_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    logger.info("Product retrieved successfully", extra={"product_id": product_id, "name": product.name})
    return product


# ----------------------------------------------------
# 3. WRITE ROUTES (POST/PATCH/DELETE)
# ----------------------------------------------------


@router.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new product to the inventory",
)
def create_product(product: ProductCreate, session: SessionDep) -> Product:
    """
    Persists a new product record.

    Validates input using ProductCreate and maps it to the Product table model.
    The database automatically handles ID generation and stock-status logic.
    """
    logger.info(
        "Creating new product", extra={"name": product.name, "price": product.price, "quantity": product.quantity, "in_stock": product.in_stock}
        )

    # 1. Converts the Pydantic schema into a SQLModel Table instance
    db_product = Product.model_validate(product)
    # 2. Add to session and commit to persist
    session.add(db_product)
    session.commit()
    session.refresh(db_product)  # Syncs db_product with the DB-generated ID

    logger.info("Product created successfully", extra={"product_id": db_product.id})
    return db_product


@router.patch(
    "/products/{product_id}",
    response_model=Product,
    summary="Partial update of a product's quantity and/or stock status",
)
def update_product(
    product_id: int, update_data: ProductUpdate, session: SessionDep
) -> Product:
    """
    Updates specific fields of an existing product.

    Uses 'exclude_unset=True' to ensure only fields provided in the
    request body are modified, preserving other existing values.
    """
    logger.info(
        "Updating product", extra={"product_id": product_id, "quantity": update_data.quantity, "in_stock": update_data.in_stock}
    )
    db_product = session.get(Product, product_id)

    if not db_product:
        # Raise 404 if the product to update was not found
        logger.warning("Product not found for update", extra={"product_id": product_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    # Update only the fields provided in update_data
    product_data = update_data.model_dump(exclude_unset=True)

    # Update the database product with the new data
    for key, value in product_data.items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    logger.info(
        "Product updated", extra={"product_id": product_id, "quantity": db_product.quantity, "in_stock": db_product.in_stock}
        )
    return db_product


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a product",
)
def delete_product(product_id: int, session: SessionDep) -> None:
    """
    Deletes a product from the database.
    Returns HTTP 204 to indicate successful deletion with no response body.
    """
    logger.info("Attempting to delete product", extra={"product_id": product_id})
    db_product = session.get(Product, product_id)

    if not db_product:
        # Raise 404 if the product to delete was not found
        logger.warning("Product not found for deletion", extra={"product_id": product_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    session.delete(db_product)
    session.commit()

    logger.info("Product deleted successfully", extra={"product_id": product_id})
    return None  # 204 No Content does not return a body