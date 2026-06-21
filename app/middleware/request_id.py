"""
Request ID middleware.
Assigns a unique ID to every request for tracing and debugging.
"""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add a unique X-Request-ID header to every request/response."""
    
    async def dispatch(self, request: Request, call_next):
        # Get existing request ID or generate new one
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Store in request state for access in endpoints
        request.state.request_id = request_id
        
        # Process request
        response: Response = await call_next(request)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
