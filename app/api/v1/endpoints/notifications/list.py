from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.notification_service import NotificationService
router = APIRouter()

@router.get("", summary="Get notifications")
async def list_notifications(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = NotificationService(db); result = await svc.get_notifications(user.id, page, per_page)
    return APIResponse(success=True, message="Notifications retrieved", data=result)
