# from typing import List, Dict, Any -> test first then implement
# from models import Product
from inventory_io import load_products, save_products


def get_next_id(products: list) -> int:
    """Get the next available product unique ID."""
    if not products:
        return 1

    max_id = max(product.get("id", 0) for product in products)
    return max_id + 1


def add_product(new_product_data: dict, inventory_data: list) -> dict:
    """Add a new product to the inventory."""
    new_id = get_next_id(inventory_data)

    product_to_add = new_product_data.copy()
    product_to_add["id"] = new_id

    inventory_data.append(product_to_add)

    save_products(inventory_data)

    return product_to_add
