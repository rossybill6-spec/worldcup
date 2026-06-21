"""
Global error handler middleware.
Catches all unhandled exceptions and returns clean JSON responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import AppException
from app.core.response import error_response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware."""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        
        except AppException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=error_response(
                    message=e.message,
                    error_code=e.error_code,
                    details=e.details,
                ),
            )
        
        except Exception as e:
            # Log the error (in production, send to logging service)
            print(f"❌ Unhandled error: {type(e).__name__}: {str(e)}")
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=error_response(
                    message="An unexpected error occurred",
                    error_code="INTERNAL_ERROR",
                ),
            )
