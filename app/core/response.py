"""
Standardized API response formats.
"""

from typing import Any, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard success response."""
    
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Any] = None


def success_response(
    data: Any = None,
    message: str = "OK",
) -> dict:
    """Create a success response dict."""
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    message: str,
    error_code: Optional[str] = None,
    details: Any = None,
) -> dict:
    """Create an error response dict."""
    return {
        "success": False,
        "message": message,
        "error_code": error_code,
        "details": details,
    }
