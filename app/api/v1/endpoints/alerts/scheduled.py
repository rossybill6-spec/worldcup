from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.alert import AlertPreferenceUpdate
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.alert_service import AlertService
router = APIRouter()
@router.get("/preferences", summary="Get alert preferences")
async def get_prefs(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = AlertService(db); prefs = await svc.get_preferences(user.id)
    return APIResponse(success=True, data=prefs)
@router.put("/preferences", summary="Update alert preferences")
async def update_prefs(data: AlertPreferenceUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = AlertService(db); await svc.update_preferences(user.id, data.model_dump(exclude_none=True))
    await db.commit(); return APIResponse(success=True, message="Alert preferences updated")
