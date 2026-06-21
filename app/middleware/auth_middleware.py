"""
Auth middleware - Validates JWT tokens on protected routes.
"""

from typing import Optional
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.tokenizers import verify_token, get_user_id_from_token


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware that validates JWT tokens on protected routes."""
    
    # Routes that don't require authentication
    PUBLIC_PATHS = [
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/health",
        "/api/v1/auth/signup",
        "/api/v1/auth/login",
        "/api/v1/auth/forgot-password",
        "/api/v1/auth/reset-password",
        "/api/v1/auth/forgot-username",
        "/api/v1/auth/refresh-token",
        "/api/v1/auth/verify-email",
        "/api/v1/auth/verify-phone",
        "/api/v1/auth/resend-verification",
        "/api/v1/auth/biometric/login",
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public paths
        path = request.url.path.rstrip("/")
        
        # Allow public paths and paths that start with public prefixes
        is_public = path in self.PUBLIC_PATHS
        is_public = is_public or path.startswith("/docs")
        is_public = is_public or path.startswith("/redoc")
        is_public = is_public or path.startswith("/openapi")
        is_public = is_public or path.startswith("/api/v1/auth/test-verification-code")
        
        if is_public:
            return await call_next(request)
        
        # Check for authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )
        
        token = auth_header.split()[1]
        user_id = get_user_id_from_token(token)
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        
        # Store user_id in request state for endpoints
        request.state.user_id = user_id
        
        return await call_next(request)
