"""
Data Access Layer (DAL) for the Retail API.

Handles all read and write operations directly with the products.json file.
"""

import json
import os
import logging

# Get logger instance for this module
logger = logging.getLogger(__name__)

# Define the filename once
INVENTORY_DATA = "products.json"


def load_products() -> list:
    """
    Loads products from the JSON file.

    Handles file not found or empty/invalid JSON by returning an empty list [].
    This ensures the API always starts with a valid data structure.
    """
    if not os.path.exists(INVENTORY_DATA):
        logger.warning(
            f"Data file {INVENTORY_DATA} not found. Initializing with empty inventory."
        )
        return []
    try:
        with open(INVENTORY_DATA, "r", encoding="utf-8") as f:
            # Use a robust check for empty file content
            content = f.read().strip()
            if not content:
                return []

            data = json.loads(content)  # Parse the string directly

            # Ensure we return a list of products, even if the JSON structure is a dictionary
            if isinstance(data, dict):
                # Convert dict values to list for safety.
                return list(data.values()) if data else []

            return data

    except json.JSONDecodeError:
        # Handle case where file exists but content is invalid JSON
        logger.error(
            f"Invalid JSON found in {INVENTORY_DATA}. Starting with empty inventory."
        )
        return []
    # Catch other unexpected errors
    except Exception as e:
        logger.critical(f"Unexpected error during product loading: {e}", exc_info=True)
        return []


def save_products(products: list):
    """
    Saves the current list of products to the JSON file.
    Overwrites the existing file content to ensure data consistency.
    """
    # Use 'products: list' to enforce type hint for clarity
    try:
        with open(INVENTORY_DATA, "w", encoding="utf-8") as f:
            # ensure_ascii=False allows proper encoding of Greek/special chars
            json.dump(products, f, indent=4, ensure_ascii=False)
        logger.info(f"Successfully saved {len(products)} products to {INVENTORY_DATA}.")
    except Exception as e:
        logger.error(f"Failed to save products to {INVENTORY_DATA}: {e}", exc_info=True)
