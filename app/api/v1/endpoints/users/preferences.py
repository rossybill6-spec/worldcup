"""
User preferences endpoints (language, theme, etc.).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


class AppPreferencesRequest(BaseModel):
    language: Optional[str] = None
    theme: Optional[str] = None
    currency_display: Optional[str] = None
    timezone: Optional[str] = None


@router.get("/preferences", response_model=APIResponse, summary="Get app preferences")
async def get_preferences(
    user: User = Depends(get_current_user),
):
    """Get user app preferences (stored client-side, placeholder)."""
    return APIResponse(success=True, message="Preferences retrieved", data={
        "language": "en", "theme": "light", "currency_display": "USD", "timezone": "UTC",
    })


@router.put("/preferences", response_model=APIResponse, summary="Update app preferences")
async def update_preferences(
    data: AppPreferencesRequest,
    user: User = Depends(get_current_user),
):
    """Update app preferences."""
    return APIResponse(success=True, message="Preferences updated", data=data.model_dump())
