"""
SQLModel Data Schemas for the Retail Inventory API.

This module defines both the database table structure AND the API data contract,
using SQLModel (combines Pydantic + SQLAlchemy).
"""

from sqlmodel import SQLModel, Field

class ProductBase(SQLModel):
    """
    Base schema for Product resource, shared attributes.
    """

    name: str = Field(max_length=50, description="Name of the product.")
    price: float = Field(gt=0, description="Unit price, must be greater than zero.")
    quantity: int = Field(default=0,ge=0, description="Current stock quantity.")
    # Auto-updated in service layer based on quantity / User can override on create
    in_stock: bool = Field(default=True, description="Stock availability flag.") 
class Product(ProductBase, table=True):
    """
    Data contract (Schema) and database table for a single Product resource.
    
    SQLModel automatically handles both Pydantic validation
    and SQLAlchemy ORM mapping.
    """
    id: int | None = Field(default=None, primary_key=True, description="Unique product identifier.")
    
class ProductCreate(ProductBase):
     """Schema for creating a new product."""
    in_stock: bool | None = None
class ProductUpdate(SQLModel):
    """Schema for partial product updates."""
    name: str | None = Field(default=None, max_length=50)
    price: float | None = Field(default=None, gt=0)
    quantity: int | None = Field(default=None, ge=0)
    in_stock: bool | None = None