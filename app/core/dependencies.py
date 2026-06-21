"""
Shared FastAPI dependencies used across endpoints.
"""

from typing import Optional
from fastapi import Depends, Query, Header, HTTPException, status

from app.core.pagination import PaginationParams


async def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginationParams:
    """Dependency to extract pagination parameters from query string."""
    return PaginationParams(page=page, per_page=per_page)


async def get_current_user_id(
    authorization: Optional[str] = Header(None),
) -> str:
    """
    Placeholder for getting current user from JWT token.
    Will be fully implemented in Phase 1 (Authentication).
    For now, returns a dummy user ID for testing.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    # Phase 1 will implement actual JWT verification here
    return "dummy-user-id"
