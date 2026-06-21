"""
Common schema types used across all API endpoints.
"""

from typing import Optional, Any
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API success response."""
    success: bool = True
    message: str = "OK"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard API error response."""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Any] = None


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
