"""
Custom exception classes for the application.
"""

from typing import Optional, Any


class AppException(Exception):
    """Base application exception."""
    
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = 400,
        error_code: Optional[str] = None,
        details: Any = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found."""
    
    def __init__(self, message: str = "Resource not found", details: Any = None):
        super().__init__(message=message, status_code=404, error_code="NOT_FOUND", details=details)


class UnauthorizedException(AppException):
    """Authentication required."""
    
    def __init__(self, message: str = "Not authenticated", details: Any = None):
        super().__init__(message=message, status_code=401, error_code="UNAUTHORIZED", details=details)


class ForbiddenException(AppException):
    """Permission denied."""
    
    def __init__(self, message: str = "Permission denied", details: Any = None):
        super().__init__(message=message, status_code=403, error_code="FORBIDDEN", details=details)


class BadRequestException(AppException):
    """Invalid request."""
    
    def __init__(self, message: str = "Bad request", details: Any = None):
        super().__init__(message=message, status_code=400, error_code="BAD_REQUEST", details=details)


class ConflictException(AppException):
    """Resource conflict (e.g., duplicate)."""
    
    def __init__(self, message: str = "Resource conflict", details: Any = None):
        super().__init__(message=message, status_code=409, error_code="CONFLICT", details=details)


class TooManyRequestsException(AppException):
    """Rate limit exceeded."""
    
    def __init__(self, message: str = "Too many requests", details: Any = None):
        super().__init__(message=message, status_code=429, error_code="RATE_LIMIT", details=details)


class ValidationException(AppException):
    """Validation error."""
    
    def __init__(self, message: str = "Validation error", details: Any = None):
        super().__init__(message=message, status_code=422, error_code="VALIDATION_ERROR", details=details)


class InsufficientFundsException(AppException):
    """Not enough balance."""
    
    def __init__(self, message: str = "Insufficient funds", details: Any = None):
        super().__init__(message=message, status_code=400, error_code="INSUFFICIENT_FUNDS", details=details)


class AccountFrozenException(AppException):
    """Account is frozen."""
    
    def __init__(self, message: str = "Account is frozen", details: Any = None):
        super().__init__(message=message, status_code=400, error_code="ACCOUNT_FROZEN", details=details)
