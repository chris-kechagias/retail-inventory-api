"""
API Gateway: FastAPI application entry point.

Defines the HTTP routes and acts as the Presentation Layer,
connecting the client requests to the Business Logic (inventory_service).
"""

# Standard Library Imports
import logging
from typing import Annotated, List, Dict, Any

# Third-Party Imports
from fastapi import FastAPI, HTTPException, status, Query
from sqlmodel import select, func

# Local/First-Party Imports
from models import Product, ProductCreate, ProductUpdate
from database import create_db_and_tables, SessionDep

# ----------------------------------------------------
# LOGGING & DATA INITIALIZATION
# ----------------------------------------------------

# Run the logging setup immediately.
import logger_config

# Get logger instance for this module (main.py)
logger = logging.getLogger(__name__)


# ----------------------------------------------------
# 1. Initialization and Data Loading
# ----------------------------------------------------

app = FastAPI(
    title="Retail Inventory API",
    description=(
        "An MVP REST API for tracking retail products, "
        "built with FastAPI and Pydantic."
    ),
    version="1.0.0",
)


# A simple log message to confirm startup
@app.on_event("startup")
def on_startup():
    logger.info("Initializing PostgreSQL database...")
    try:
        create_db_and_tables()
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


# ----------------------------------------------------
# 2. Endpoints (Analytics Route + GET Routes)
# ----------------------------------------------------


@app.get(
    "/products/total_value",
    summary="Calculate the total monetary value of the current inventory",
    response_model=Dict[str, float],
)
def get_inventory_value(session: SessionDep):
    """
    Calculate the total value of all products in stock.

    Performs the calculation (price * quantity) directly within the
    SQL engine for maximum performance. Returns 0.0 if the inventory is empty.
    """
    logger.info("Calculating total inventory value via database-side aggregation")

    statement = select(func.sum(Product.price * Product.quantity))

    result = session.exec(statement).one()
    total_value = result or 0.0

    logger.info(f"Total inventory value successfully calculated: ${total_value:.2f}")

    return {"Total Inventory Value $": total_value}


@app.get(
    "/products",
    response_model=List[Product],
    summary="Retrieve all products in the inventory",
)
def get_all_products(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    """
    GET /products
    Returns the complete list of all products in the inventory.
    """
    statement = select(Product).offset(offset).limit(limit)
    products = session.exec(statement).all()
    logger.info(f"Fetching products: offset={offset}, limit={limit}")
    return products


@app.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Retrieve a single product by its unique ID",
)
def get_product(product_id: int, session: SessionDep) -> Product:
    """
    GET /products/{product_id}
    Returns a single product by its unique ID. Raises 404 if not found.
    """
    logger.info(f"Fetching product with ID: {product_id}")
    product = session.get(Product, product_id)

    if not product:
        # Raise the standard HTTP 404 if not found
        logger.warning(f"Product {product_id} not found - returning 404")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    logger.info(f"Product {product_id} found: {product.name}")
    return product


# ----------------------------------------------------
# 3. Endpoints (POST Routes)
# ----------------------------------------------------


@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new product to the inventory",
)
def create_product(product: ProductCreate, session: SessionDep) -> Product:
    """
    Create a new product in the database.

    The input uses ProductCreate (no ID required), and the database
    automatically generates a unique primary key upon commit.
    """
    logger.info(
        f"Creating new product: {product.name} (price: ${product.price}, quantity: {product.quantity})"
    )

    # 1. Convert ProductCreate (Schema) to Product (Database Model)
    db_product = Product.model_validate(product)
    # 2. Add to session and commit to persist
    session.add(db_product)
    session.commit()
    session.refresh(db_product)  # Refresh to get the generated ID

    logger.info(f"Product created successfully with ID: {db_product.id}")
    return db_product


# ----------------------------------------------------
# 4. Endpoints (PUT Route)
# ----------------------------------------------------


@app.patch(
    "/products/{product_id}",
    response_model=Product,
    summary="Update the quantity of an existing product",
)
def update_product(
    product_id: int, update_data: ProductUpdate, session: SessionDep
) -> Product:
    """
    Updates the quantity of an existing product by ID.
    Raises 404 if the product is not found.
    """
    logger.info(
        f"Updating product {product_id} with new quantity: {update_data.quantity}"
    )
    db_product = session.get(Product, product_id)

    if not db_product:
        # Raise 404 if the product to update was not found
        logger.warning(f"Product {product_id} not found for update - returning 404")
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
        f"Product {product_id} updated successfully (new quantity: {db_product.quantity}, in_stock: {db_product.in_stock})"
    )
    return db_product


# ----------------------------------------------------
# 5. Endpoints (DELETE Route)
# ----------------------------------------------------


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product from the inventory",
)
def delete_product_endpoint(product_id: int) -> None:
    """
    Deletes a product by its unique ID.
    Raises 404 if the product is not found.
    """
    logger.info(f"Attempting to delete product {product_id}")

    deleted = delete_product(product_id=product_id, inventory_data=INVENTORY_DATA)

    if not deleted:
        # Raise 404 if the product to delete was not found
        logger.warning(f"Product {product_id} not found for deletion - returning 404")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    logger.info(f"Product {product_id} deleted successfully")
    return None  # 204 No Content does not return a body
