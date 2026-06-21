from typing import Optional
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.tokenizers import get_user_id_from_token

class AuthMiddleware(BaseHTTPMiddleware):
    PUBLIC_PREFIXES = [
        "/docs", "/redoc", "/openapi.json", "/favicon.ico",
        "/api/v1/auth/signup", "/api/v1/auth/login", "/api/v1/auth/verify-email",
        "/api/v1/auth/forgot-password", "/api/v1/auth/reset-password",
        "/api/v1/auth/forgot-username", "/api/v1/auth/refresh-token",
        "/api/v1/auth/test-verification-code", "/api/v1/auth/biometric/login",
        "/api/v1/health",
    ]
    
    async def dispatch(self, request: Request, call_next):
        path = request.url.path.rstrip("/")
        if path == "/" or any(path.startswith(p) for p in self.PUBLIC_PREFIXES):
            return await call_next(request)
        auth = request.headers.get("authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        token = auth.split()[1]
        user_id = get_user_id_from_token(token)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        request.state.user_id = user_id
        return await call_next(request)
