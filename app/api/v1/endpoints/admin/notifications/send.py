from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.notification_service import NotificationService
router = APIRouter()

class SendNotificationRequest(BaseModel):
    user_id: str = Field(None); title: str; message: str
    notification_type: str = "admin"; send_to_all: bool = False

@router.post("/send", summary="Send notification to user(s)")
async def send_notification(data: SendNotificationRequest, db: AsyncSession = Depends(get_db)):
    svc = NotificationService(db)
    if data.send_to_all:
        from sqlalchemy import select
        from app.models.user import User
        users = (await db.execute(select(User.id).where(User.is_active == True))).scalars().all()
        for uid in users:
            await svc.send(uid, data.title, data.message, data.notification_type)
    elif data.user_id:
        await svc.send(data.user_id, data.title, data.message, data.notification_type)
    await db.commit()
    return APIResponse(success=True, message="Notification sent")
