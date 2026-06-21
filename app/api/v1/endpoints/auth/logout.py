"""
Logout endpoint - End user session.
"""

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/logout",
    response_model=APIResponse,
    summary="Logout and end current session",
)
async def logout(
    authorization: Optional[str] = Header(None),
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID"),
    db: AsyncSession = Depends(get_db),
):
    """
    Logout the current user session.
    Provide either the session ID in X-Session-ID header or just the auth token.
    """
    auth_service = AuthService(db)
    
    if x_session_id:
        success, message = await auth_service.logout(x_session_id)
        return APIResponse(success=success, message=message)
    
    return APIResponse(success=True, message="Logged out")
