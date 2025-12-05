# This is an attempt for Inventory Tracker 2.0
# Main purpose is to build a Retail API
# By using and testing new acquired knowledge

# ==== Main functions of Inventory Tracker CLI ===
# 1.View all products --> GET /products (ex inventory.py | main menu/loop)
#   |
#   --> View a single product  --> GET /products/{id} (need to write a function for this)
# 2.Add a new product --> POST /products (ex add_product | inventory_services.py)
# 3.Update product quantity --> PUT /products/{id} (ex add_product | inventory_services.py)
# 4.Delete a product --> DELETE /products/{id} (ex add_product | inventory_services.py)
# 5.Calculate total value of inventory --> GET /products/total_value (ex add_product | inventory_services.py)
# 6. Exit
# ================================================

# A) Define the Pydantic Product model --> models.py --- Done
# B) Set up FastAPI app and endpoints --> main.py
# C) Import my CLI's load_products and save_products functions --> iventory_io.py
# D) Implement each CLI function to interact with the FastAPI endpoints using HTTP requests --> main.py
#    |--> Implement GET /products (lists all)
#    |--> Implement GET /products/{id} (gets single-don't forget error handling if the ID is not found, e.g., raising an HTTPException)
#    |--> Implement POST /products (adds new, uses Pydantic model)
#    |--> Implement PUT /products/{id} (updates quantity, also with error handling)
#    |--> Implement DELETE /products/{id} (deletes product, with error handling
#    |--> Implement GET /products/total_value (calculates total inventory value)


# Establishing Three-Tier Architecture
#    |--> Presentation Layer: FastAPI endpoints (main.py)
#    |--> Business Logic Layer: Inventory services (inventory_services.py)
#    |--> Data Access Layer: File I/O operations (inventory_io.py)

"""
API Gateway: FastAPI application entry point.

Defines the HTTP routes and acts as the Presentation Layer,
connecting the client requests to the Business Logic (inventory_service).
"""
from fastapi import FastAPI, HTTPException, status
from typing import List, Dict, Any

# Import the Pydantic Product model and data access functions
from models import Product
from inventory_io import load_products

# ----------------------------------------------------
# 1. Initialization and Data Loading
# ----------------------------------------------------

app = FastAPI(
    title="Retail Inventory API",
    description="An MVP REST API for tracking retail products, built with FastAPI and Pydantic.",
    version="0.1.0",
)

# Load initial products from the JSON file
INVENTORY_DATA: List[Dict[str, Any]] = load_products()

# ----------------------------------------------------
# 2. Endpoints (GET Routes)
# ----------------------------------------------------


@app.get(
    "/products",
    response_model=List[Product],
    summary="Retrieve all products in the inventory",
)
def get_all_products():
    """
    GET /products
    Returns a list of all products in the inventory.
    """
    return INVENTORY_DATA


@app.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Retrieve a single product by its unique ID",
)
def get_product(product_id: int):
    """
    GET /products/{product_id}
    Returns a single product by its unique ID.
    """
    for product in INVENTORY_DATA:
        if product["id"] == product_id:
            return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with ID {product_id} not found.",
    )
