"""
API Gateway: FastAPI application entry point.

This module defines the RESTful endpoints for the Retail Inventory system.
It acts as the Presentation Layer, handling HTTP requests/responses and
orchestrating data persistence through SQLModel and PostgreSQL.
"""

# Standard Library Imports
import logging
import time
from contextlib import asynccontextmanager
from typing import Annotated, Dict, List #!

# Third-Party Imports
from fastapi import FastAPI, HTTPException, Query, status #!
from sqlmodel import func, select #!

# Local/First-Party Imports
import app.logger_config  # noqa: F401
from app.database import SessionDep, create_db_and_tables #!
from app.models import HealthResponse, Product, ProductCreate, ProductUpdate #!
from app.routers import products

# ----------------------------------------------------
# LOGGING & INITIALIZATION
# ----------------------------------------------------
START_TIME = time.time()


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles the application startup and shutdown events.

    Ensures the database engine is ready and tables are created before
    the API starts accepting traffic. This replaces the deprecated @app.on_event logic.
    """
    logger.info(
        "Lifespan Startup: Verifying database connectivity and creating tables."
    )
    # This replaces the old @app.on_event("startup") logic.
    # It ensures the database is ready before the first request arrives.
    create_db_and_tables()
    yield
    logger.info("Lifespan Shutdown: Cleaning up resources.")


app = FastAPI(
    title="Retail Inventory API",
    description="A robust FastAPI service for managing warehouse stock using PostgreSQL and SQLModel.",
    version="1.2.0",  # Updated to reflect Mock tests, input validation, structured JSON logging milestone
    lifespan=lifespan,
)

app.include_router(products.router)

@app.head("/health")
@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    return HealthResponse(
        status="healthy",
        version="1.2.0",
        uptime=time.time() - START_TIME
    )

@app.get("/")
def read_root():
    return {
        "message": "Retail Inventory API",
        "version": "1.2.0",
        "docs": "/docs",
        "endpoints": "/products"
    }



# ----------------------------------------------------
# 2. READ ROUTES
# ----------------------------------------------------


@app.get(
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


@app.get(
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


@app.post(
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


@app.patch(
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


@app.delete(
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
