"""
User limits endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user_limit import LimitResponse
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/limits", response_model=APIResponse, summary="Get account limits")
async def get_limits(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current account limits."""
    limits = LimitResponse()
    return APIResponse(success=True, message="Limits retrieved", data=limits.model_dump())
