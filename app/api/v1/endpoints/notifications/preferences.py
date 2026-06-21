from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.notification import NotificationPreferencesUpdate
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.models.user_notification_preference import UserNotificationPreference
from sqlalchemy import select
router = APIRouter()

@router.get("/preferences", summary="Get notification preferences")
async def get_prefs(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(UserNotificationPreference).where(UserNotificationPreference.user_id == user.id))
    prefs = r.scalar_one_or_none()
    if not prefs: return APIResponse(success=True, data={})
    return APIResponse(success=True, data={"push_enabled":prefs.push_enabled,"email_enabled":prefs.email_enabled,"sms_enabled":prefs.sms_enabled})

@router.put("/preferences", summary="Update notification preferences")
async def update_prefs(data: NotificationPreferencesUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(UserNotificationPreference).where(UserNotificationPreference.user_id == user.id))
    prefs = r.scalar_one_or_none()
    if prefs:
        for k,v in data.model_dump(exclude_none=True).items(): setattr(prefs, k, v)
    await db.commit(); return APIResponse(success=True, message="Preferences updated")
