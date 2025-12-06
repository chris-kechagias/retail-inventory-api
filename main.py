# This is an attempt for Inventory Tracker 2.0
# Main purpose is to build a Retail API
# By using and testing new acquired knowledge

# ==== Main functions of Inventory Tracker CLI ===
# 1.View all products --> GET /products
#   (ex inventory.py | main menu/loop) --- Done
#   |
#   --> View a single product  --> GET /products/{id}
#       (need to write a function for this) --- Done
# 2.Add a new product --> POST /products
#   (ex add_product | inventory_services.py) --- Done
# 3.Update product quantity --> PUT /products/{id}
#    (ex update_product_quantity | inventory_services.py) --- Done
# 4.Delete a product --> DELETE /products/{id}
#   (ex delete_product | inventory_services.py) --- Done
# 4.Delete a product --> DELETE /products/{id}
#   (ex delete_product | inventory_services.py) --- Done
# 5.Calculate total value of inventory --> GET /products/total_value
#   (ex add_product | inventory_services.py) was a bonus function
# 6. Exit
# ================================================

# A) Define the Pydantic Product model --> models.py --- Done
# B) Set up FastAPI app and endpoints --> main.py --- Done
# C) Import my CLI's load_products and save_products functions
#    --> inventory_io.py --- Done
# D) Implement inventory service functions --> inventory_service.py --- Done
#    |--> Implement get_next_id (to assign unique IDs to new products) --- Done
#    |--> Implement add_product (to add new products to inventory) --- Done
#    |--> Implement update_product_quantity (to update quantity of
#         existing products) --- Done
#    |--> Implement delete_product (to remove products from inventory) --- Done
# E) Implement each CLI function to interact with the FastAPI
#    endpoints using HTTP requests --> main.py
#    |--> Implement GET /products (lists all) --- Done
#    |--> Implement GET /products/{id} (gets single product with error
#         handling if the ID is not found, e.g., raising HTTPException)
#         --- Done
#    |--> Implement POST /products (adds new, uses Pydantic model) --- Done
#    |--> Implement PUT /products/{id} (updates quantity, with
#         error handling) --- Done
#    |--> Implement DELETE /products/{id} (deletes product, with
#         error handling) --- Done
#    |--> Implement GET /products/total_value (calculates total
#         inventory value) --- Done


# Establishing Three-Tier Architecture
#    |--> Presentation Layer: FastAPI endpoints (main.py) --- Done
#    |--> Business Logic Layer: Inventory services
#         (inventory_services.py) --- Done
#    |--> Data Access Layer: File I/O operations (inventory_io.py) --- Done

"""
API Gateway: FastAPI application entry point.

Defines the HTTP routes and acts as the Presentation Layer,
connecting the client requests to the Business Logic (inventory_service).
"""
# Standard Library Imports
import logging
from typing import List, Dict, Any

# Third-Party Imports
from fastapi import FastAPI, HTTPException, status

# Local/First-Party Imports
from models import Product, ProductUpdate
from inventory_io import load_products
from inventory_service import (
    add_product,
    update_product_quantity,
    delete_product,
    calculate_total_inventory_value,
)

# ----------------------------------------------------
# LOGGING & DATA INITIALIZATION
# ----------------------------------------------------

# Run the logging setup immediately.
import logger_config

# Get logger instance for this module (main.py)
logger = logging.getLogger(__name__)

# Global In-Memory State for Inventory Data
INVENTORY_DATA = load_products()

# ----------------------------------------------------
# 1. Initialization and Data Loading
# ----------------------------------------------------

app = FastAPI(
    title="Retail Inventory API",
    description=(
        "An MVP REST API for tracking retail products, "
        "built with FastAPI and Pydantic."
    ),
    version="0.1.0",
)


# A simple log message to confirm startup
@app.on_event("startup")
def startup_event():
    logger.info("Retail API Server Starting Up")
    # Log the initial inventory size
    logger.info(f"Initial inventory loaded with {len(INVENTORY_DATA)} products.")


# ----------------------------------------------------
# 2. Endpoints (Analytics Route + GET Routes)
# ----------------------------------------------------


@app.get(
    "/products/total_value",
    summary="Calculate the total monetary value of the current inventory",
    response_model=Dict[str, float],
)
def get_inventory_value():
    """
    Returns a dictionary containing the sum of (price * quantity) for all products.
    """
    total_value = calculate_total_inventory_value(inventory_data=INVENTORY_DATA)
    return {"total_value": total_value}


@app.get(
    "/products",
    response_model=List[Product],
    summary="Retrieve all products in the inventory",
)
def get_all_products():
    """
    GET /products
    Returns the complete list of all products in the inventory.
    """
    # FastAPI/Pydantic automatically validates and converts the list of dictionaries
    # into the Product schema for the response.
    return INVENTORY_DATA


@app.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Retrieve a single product by its unique ID",
)
def get_product(product_id: int) -> Product:
    """
    GET /products/{product_id}
    Returns a single product by its unique ID. Raises 404 if not found.
    """
    # Temporary logic: Searching directly in the list
    # (will move to the service layer later)

    for product in INVENTORY_DATA:
        if product["id"] == product_id:
            return product
    # Raise the standard HTTP 404 if not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with ID {product_id} not found.",
    )


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
    # Call the Service Layer for business logic
    created_product = add_product(
        # We use .model_dump() to convert the Pydantic object back into a
        # standard Python dict
        new_product_data=product.model_dump(),
        inventory_data=INVENTORY_DATA,  # Pass the global in-memory state
    )

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
    updated_product = update_product_quantity(
        product_id=product_id,
        new_quantity=update_data.quantity,
        inventory_data=INVENTORY_DATA,
    )

    if updated_product is None:
        # Raise 404 if the product to update was not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
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
def delete_product_endpoint(product_id: int):
    """
    Deletes a product by its unique ID.
    Raises 404 if the product is not found.
    """
    deleted = delete_product(product_id=product_id, inventory_data=INVENTORY_DATA)

    if not deleted:
        # Raise 404 if the product to delete was not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    return None  # 204 No Content does not return a body
