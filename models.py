"""
Pydantic Data Schemas for the Retail Inventory API.

This module defines the data contract for all API requests and responses,
ensuring data integrity and type safety across the service.
"""

from pydantic import BaseModel, Field

# from typing import  Optional  Not strictly needed here, but good practice to keep the import for reference


class Product(BaseModel):
    """
    Data contract (Schema) for a single Product resource.

    Defines the required fields and validation rules (e.g., price > 0, quantity >= 0)
    for data traveling through the API endpoints.
    """

    # ID: Number, must be positive.
    id: int = Field(..., gt=0, description="Unique product identifier.")

    # Name: String, maximum length 50 characters.
    name: str = Field(..., max_length=50, description="Name of the product.")

    # Price: Float, must be strictly greater than zero.
    price: float = Field(
        ..., gt=0, description="Unit price, must be greater than zero."
    )

    # Quantity: Integer, must be greater than or equal to 0 (can be out of stock).
    quantity: int = Field(..., ge=0, description="Current stock quantity.")

    # In Stock: Calculated in service layer when quantity changes.
    # Default True for new products (most items start in stock).
    in_stock: bool = Field(
        default=True,
        description="Stock availability flag. Auto-updated in service layer based on quantity.",
    )


class ProductUpdate(BaseModel):
    """Schema for partial product updates (only quantity in MVP)."""

    quantity: int = Field(..., ge=0, description="New quantity, must be non-negative.")


# Future fields for updates can be added here
