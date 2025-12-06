"""
Business Logic Layer (BLL) for the Retail API.

Handles core operations like adding products
"""

# from typing import List, Dict, Any -> test first then implement
# from models import Product
from inventory_io import save_products  # load_products,


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

    return product_to_add


# Future functions like update_product_quantity can be added here
