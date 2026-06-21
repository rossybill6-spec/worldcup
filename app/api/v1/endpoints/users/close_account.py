"""
Account closure endpoint.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()


class CloseAccountRequest(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500)
    destination_account: Optional[str] = Field(None, max_length=50)
    confirm: bool = Field(..., description="Must be true")


@router.post("/close-account", response_model=APIResponse, summary="Close account")
async def close_account(
    data: CloseAccountRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Permanently close your account."""
    if not data.confirm:
        return APIResponse(success=False, message="You must confirm account closure")
    
    service = UserService(db)
    success, message = await service.close_account(user.id, data.reason, data.destination_account)
    await db.commit()
    return APIResponse(success=success, message=message)
