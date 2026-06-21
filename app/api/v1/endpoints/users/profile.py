"""
User profile endpoints - View and edit profile.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user_profile import UpdateProfileRequest, ProfileResponse
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()


@router.get("/profile", response_model=APIResponse, summary="Get user profile")
async def get_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the authenticated user's full profile."""
    service = UserService(db)
    profile = await service.get_profile(user.id)
    return APIResponse(success=True, message="Profile retrieved", data=profile)


@router.put("/profile", response_model=APIResponse, summary="Update user profile")
async def update_profile(
    data: UpdateProfileRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update profile fields."""
    service = UserService(db)
    await service.update_profile(user.id, data.model_dump(exclude_none=True))
    profile = await service.get_profile(user.id)
    return APIResponse(success=True, message="Profile updated", data=profile)
