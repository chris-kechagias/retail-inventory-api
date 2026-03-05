from datetime import datetime, timezone
from typing import Any, Dict

from exceptions import AppException, ValidationException


def create_error_response(exception: AppException) -> Dict[str, Any]:
    """Helper function to create a standardized error response from an AppException."""
    response = {
        "success": False,
        "error": {
            "code": exception.error_code,
            "message": exception.message,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }

    if exception.details:
        response["error"]["details"] = exception.details

    return response


async def app_exception_handler(request, exception: AppException):
    # log + return JSONResponse
    pass


async def validation_exception_handler(request, exception: ValidationException):
    # log + return JSONResponse
    pass
