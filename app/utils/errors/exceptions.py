"""
Custom exceptions for the application,
providing structured error information for API responses.
Each exception includes a message, HTTP status code, error code, and optional details.

"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AppException(Exception):
    """Base exception for all application errors"""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ProductNotFoundException(AppException):
    def __init__(self, product_id: int):
        super().__init__(
            message=f"Product with ID {product_id} not found",
            status_code=404,
            error_code="PRODUCT_NOT_FOUND",
        )
        self.product_id = product_id


class ProductVariantNotFoundException(AppException):
    def __init__(self, variant_id: int):
        super().__init__(
            message=f"Variant with ID {variant_id} not found",
            status_code=404,
            error_code="VARIANT_NOT_FOUND",
        )
        self.variant_id = variant_id


class ValidationException(AppException):
    def __init__(self, details: dict):
        super().__init__(
            message="Validation error",
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class DatabaseException(AppException):
    def __init__(
        self, message: str = "Database error", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
            details=details,
        )


class ErrorDetail(BaseModel):
    code: str
    message: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail
