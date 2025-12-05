"""
Data Access Layer (DAL) for the Retail API.

Handles all read and write operations directly with the products.json file.
"""

import json
import os

# Define the filename once
INVENTORY_DATA = "products.json"


def load_products() -> list:
    """
    Loads products from the JSON file.

    Handles file not found or empty/invalid JSON by returning an empty list [].
    This ensures the API always starts with a valid data structure.
    """
    if not os.path.exists(INVENTORY_DATA):
        # File doesn't exist, start with an empty list
        return []
    try:
        with open(INVENTORY_DATA, "r", encoding="utf-8") as f:
            # Use a robust check for empty file content
            content = f.read().strip()
            if not content:
                return []

            # Reset file pointer and load the content
            f.seek(0)
            data = json.load(f)

            # Ensure we return a list of products, even if the JSON structure is a dictionary
            if isinstance(data, dict):
                # Convert dict values to list for safety.
                return list(data.values()) if data else []

            return data

    except json.JSONDecodeError:
        # Handle case where file exists but content is invalid JSON
        print(
            f"Warning: Invalid JSON found in {INVENTORY_DATA}. Starting with empty inventory."
        )
        return []
    # Catch other unexpected errors
    except Exception as e:
        print(f"An unexpected error occurred while loading products: {e}")
        return []


def save_products(products: list):
    """
    Saves the current list of products to the JSON file.
    Overwrites the existing file content to ensure data consistency.
    """
    # Use 'products: list'to enforce type hint for clarity
    with open(INVENTORY_DATA, "w", encoding="utf-8") as f:
        # The ensure_ascii=False allows for proper encoding of Greek/special characters
        json.dump(products, f, indent=4, ensure_ascii=False)
