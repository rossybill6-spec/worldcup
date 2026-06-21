"""
Session management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()


@router.get("/sessions", response_model=APIResponse, summary="List active sessions")
async def list_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all active sessions."""
    service = UserService(db)
    sessions = await service.get_sessions(user.id)
    return APIResponse(success=True, message="Sessions retrieved", data=sessions)


@router.delete("/sessions/{session_id}", response_model=APIResponse, summary="Revoke session")
async def revoke_session(
    session_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Revoke a specific session (logout from that device)."""
    service = UserService(db)
    success = await service.revoke_session(user.id, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return APIResponse(success=True, message="Session revoked")
