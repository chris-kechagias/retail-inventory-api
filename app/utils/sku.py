"""
SKU generation utility.

A SKU (Stock Keeping Unit) is a human-readable identifier used in retail
to track products. Format: <CATEGORY_PREFIX>-<ZERO_PADDED_NUMBER>
Example: TS-0001 (first Tee), SW-0003 (third Sweater).
"""

from app.models.product import Category

# Mapping from category enum to its 2-letter SKU prefix
CATEGORY_PREFIX: dict[Category, str] = {
    Category.TEES: "TS",
    Category.SWEATERS: "SW",
    Category.SHIRTS: "ST",
    Category.PANTS: "PT",
    Category.SHORTS: "SH",
    Category.TANK_TOPS: "TT",
    Category.OTHER: "OR",
}


def generate_sku(category: Category, count: int) -> str:
    """
    Generate a SKU from a category and a sequential count.

    Args:
        category: The product category (used to pick the prefix).
        count: The 1-based sequential number within that category.

    Returns:
        A SKU string like 'TS-0001' or 'SW-0042'.
    """
    prefix = CATEGORY_PREFIX[category]
    return f"{prefix}-{count:04d}"
