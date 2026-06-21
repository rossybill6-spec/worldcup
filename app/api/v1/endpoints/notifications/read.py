from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.notification_service import NotificationService
router = APIRouter()

@router.put("/{notification_id}/read", summary="Mark notification as read")
async def mark_read(notification_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = NotificationService(db); await svc.mark_read(notification_id, user.id)
    await db.commit(); return APIResponse(success=True, message="Marked as read")

@router.put("/read-all", summary="Mark all as read")
async def mark_all_read(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = NotificationService(db); await svc.mark_all_read(user.id)
    await db.commit(); return APIResponse(success=True, message="All marked as read")

@router.delete("/{notification_id}", summary="Delete notification")
async def delete_notification(notification_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = NotificationService(db); await svc.delete(notification_id, user.id)
    await db.commit(); return APIResponse(success=True, message="Notification deleted")
