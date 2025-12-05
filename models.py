"""
Pydantic Data Schemas for the Retail Inventory API.

This module defines the data contract for all API requests and responses,
ensuring data integrity and type safety across the service.
"""

from pydantic import BaseModel, Field
from typing import (
    Optional,
)  # Not strictly needed here, but good practice to keep the import for reference


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

    # In Stock: Tracks stock status. Default is True.
    # Note: You can automatically calculate this based on 'quantity' in your service layer
    # or keep it as a simple status flag for ease of use.
    in_stock: bool = Field(
        True,
        description="Boolean flag indicating if the product is currently in stock (quantity > 0).",
    )
