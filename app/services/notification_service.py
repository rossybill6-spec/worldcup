from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.notification_repository import NotificationRepository
from app.models.notification import Notification

class NotificationService:
    def __init__(self, db: AsyncSession): self.db = db; self.repo = NotificationRepository(db)
    
    async def send(self, user_id: str, title: str, message: str, notification_type: str, reference_type: str = None, reference_id: str = None) -> Notification:
        n = Notification(user_id=user_id, title=title, message=message, notification_type=notification_type, reference_type=reference_type, reference_id=reference_id)
        return await self.repo.create(n)
    
    async def get_notifications(self, user_id: str, page: int = 1, per_page: int = 20) -> Dict:
        offset = (page-1)*per_page
        notifications = await self.repo.get_by_user(user_id, per_page, offset)
        unread = await self.repo.get_unread_count(user_id)
        items = [{"id": n.id, "title": n.title, "message": n.message, "notification_type": n.notification_type, "is_read": n.is_read, "reference_type": n.reference_type, "reference_id": n.reference_id, "created_at": n.created_at.isoformat() if n.created_at else None} for n in notifications]
        return {"items": items, "unread_count": unread, "page": page, "per_page": per_page}
    
    async def mark_read(self, notification_id: str, user_id: str): await self.repo.mark_read(notification_id, user_id)
    async def mark_all_read(self, user_id: str): await self.repo.mark_all_read(user_id)
    async def delete(self, notification_id: str, user_id: str): await self.repo.delete(notification_id, user_id)
