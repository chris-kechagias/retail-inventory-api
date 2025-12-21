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
def create_product(product: Product):
    """
    Receives product data, assigns a unique ID, and saves it to the inventory.

    The Pydantic 'Product' model automatically validates the input data (e.g.,
    price and quantity are > 0).
    """
    logger.info(
        f"Creating new product: {product.name} (price: ${product.price}, quantity: {product.quantity})"
    )

    # Call the Service Layer for business logic
    created_product = add_product(
        # We use .model_dump() to convert the Pydantic object back into a
        # standard Python dict
        new_product_data=product.model_dump(),
        inventory_data=INVENTORY_DATA,  # Pass the global in-memory state
    )

    logger.info(f"Product created successfully with ID: {created_product['id']}")
    return created_product


# ----------------------------------------------------
# 4. Endpoints (PUT Route)
# ----------------------------------------------------


@app.put(
    "/products/{product_id}",
    response_model=Product,
    summary="Update the quantity of an existing product",
)
def update_product(product_id: int, update_data: ProductUpdate):
    """
    Updates the quantity of an existing product by ID.
    Raises 404 if the product is not found.
    """
    logger.info(
        f"Updating product {product_id} with new quantity: {update_data.quantity}"
    )

    updated_product = update_product_quantity(
        product_id=product_id,
        new_quantity=update_data.quantity,
        inventory_data=INVENTORY_DATA,
    )

    if updated_product is None:
        # Raise 404 if the product to update was not found
        logger.warning(f"Product {product_id} not found for update - returning 404")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    logger.info(
        f"Product {product_id} updated successfully (new quantity: {updated_product['quantity']}, in_stock: {updated_product['in_stock']})"
    )
    return updated_product


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
