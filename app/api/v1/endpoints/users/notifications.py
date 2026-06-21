"""
Notification preferences endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_notification_preference import UserNotificationPreference

router = APIRouter()


class UpdateNotificationPreferencesRequest(BaseModel):
    push_enabled: Optional[bool] = None
    push_deposits: Optional[bool] = None
    push_withdrawals: Optional[bool] = None
    push_transfers: Optional[bool] = None
    push_security: Optional[bool] = None
    email_enabled: Optional[bool] = None
    email_deposits: Optional[bool] = None
    email_withdrawals: Optional[bool] = None
    email_transfers: Optional[bool] = None
    email_security: Optional[bool] = None
    email_statements: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    sms_deposits: Optional[bool] = None
    sms_withdrawals: Optional[bool] = None
    sms_security: Optional[bool] = None


@router.get("/notifications/preferences", response_model=APIResponse, summary="Get notification preferences")
async def get_preferences(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get notification preferences."""
    result = await db.execute(
        select(UserNotificationPreference).where(UserNotificationPreference.user_id == user.id)
    )
    prefs = result.scalar_one_or_none()
    if not prefs:
        return APIResponse(success=True, message="Preferences not set", data={})
    
    return APIResponse(success=True, message="Preferences retrieved", data={
        "push_enabled": prefs.push_enabled, "push_deposits": prefs.push_deposits,
        "push_withdrawals": prefs.push_withdrawals, "push_transfers": prefs.push_transfers,
        "push_security": prefs.push_security,
        "email_enabled": prefs.email_enabled, "email_deposits": prefs.email_deposits,
        "email_withdrawals": prefs.email_withdrawals, "email_transfers": prefs.email_transfers,
        "email_security": prefs.email_security, "email_statements": prefs.email_statements,
        "sms_enabled": prefs.sms_enabled, "sms_deposits": prefs.sms_deposits,
        "sms_withdrawals": prefs.sms_withdrawals, "sms_security": prefs.sms_security,
    })


@router.put("/notifications/preferences", response_model=APIResponse, summary="Update notification preferences")
async def update_preferences(
    data: UpdateNotificationPreferencesRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update notification preferences."""
    result = await db.execute(
        select(UserNotificationPreference).where(UserNotificationPreference.user_id == user.id)
    )
    prefs = result.scalar_one_or_none()
    
    update_data = data.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(prefs, key, value)
    
    await db.commit()
    return APIResponse(success=True, message="Preferences updated")
