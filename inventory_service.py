"""
Business Logic Layer (BLL) for the Retail API.

Contains all core business rules, such as generating new IDs,
updating inventory, and calculating metrics.
"""

# from models import Product
from typing import List, Dict, Any, Optional
import logging
from inventory_io import save_products  # load_products,

# Get logger instance for this module
logger = logging.getLogger(__name__)


def get_next_id(products: list) -> int:
    """
    Calculates and returns the next available unique ID for a new product.

    Args:
        products: The current list of inventory dictionaries (in-memory state).

    Returns:
        The next sequential integer ID (e.g., if max ID is 5, returns 6).
    """
    if not products:
        return 1
    # Efficiently finds the maximum ID in the current list
    max_id = max(product.get("id", 0) for product in products)
    return max_id + 1


def add_product(new_product_data: dict, inventory_data: list) -> dict:
    """
    Adds a new product to the inventory by assigning a unique ID and
    persisting the data.

    Args:
        new_product_data: A dictionary containing the product details
            (name, price, quantity) without an 'id' field.
        inventory_data: The list holding the current in-memory state of
            the inventory.

    Returns:
        The dictionary of the newly created product, including the assigned ID.
    """
    # 1. Get the next available ID
    new_id = get_next_id(inventory_data)

    # 2. Create the final dictionary, adding the assigned ID
    product_to_add = new_product_data.copy()
    product_to_add["id"] = new_id

    # 3. Add to the in-memory list
    # (This modifies the INVENTORY_DATA in main.py)
    inventory_data.append(product_to_add)

    # 4. Save the entire list to the JSON file (DAL call)
    save_products(inventory_data)

    logger.info(
        f"Product added successfully: ID {new_id}, Name: {product_to_add['name']}"
    )

    return product_to_add


def update_product_quantity(
    product_id: int, new_quantity: int, inventory_data: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Updates the quantity of an existing product and saves the data.

    Returns the updated product dictionary, or None if the product is
    not found.
    """
    try:
        # Use a generator expression to find the product efficiently
        product_to_update = next(
            product for product in inventory_data if product["id"] == product_id
        )
        # 1. Update the quantity
        product_to_update["quantity"] = new_quantity

        # 2. Update the in_stock status based on the new quantity
        product_to_update["in_stock"] = new_quantity > 0

        # 3. Persist the changes to the file
        save_products(inventory_data)

        return product_to_update
    except StopIteration:
        # Product with the given ID was not found
        return None


def delete_product(product_id: int, inventory_data: List[Dict[str, Any]]) -> bool:
    """
    Removes a product from the inventory list and saves the changes.

    Returns True if the product was deleted, False otherwise.
    """
    # 1. Find the index of the product to delete
    for i, product in enumerate(inventory_data):
        if product["id"] == product_id:
            # 2. Remove the product from the list by index
            inventory_data.pop(i)
            # 3. Persist the changes to the file
            save_products(inventory_data)
            logger.info(f"Product {product_id} deleted successfully")
            return True

    logger.warning(f"Attempted to delete non-existent product {product_id}")
    return False


def calculate_total_inventory_value(inventory_data: List[Dict[str, Any]]) -> float:
    """
    Calculates the total monetary value of all products in the inventory.
    Value is calculated as: sum(price * quantity) for all items.
    """
    total_value = 0.0
    for product in inventory_data:
        try:
            price = product.get("price", 0.0)
            quantity = product.get("quantity", 0)
            total_value += price * quantity
        except TypeError:
            # This handles cases where price or quantity might be none or non-numeric
            logger.warning(
                "Skipping product ID %s due to invalid price or " "quantity data.",
                product.get("id"),
            )
            continue

    # Log the successful calculation
    logger.info("Total inventory value calculated: $%.2f", total_value)

    return round(total_value, 2)
