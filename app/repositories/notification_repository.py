from typing import List
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification

class NotificationRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create(self, n: Notification) -> Notification: self.db.add(n); await self.db.flush(); return n
    async def get_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> List[Notification]:
        r = await self.db.execute(select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc()).offset(offset).limit(limit))
        return list(r.scalars().all())
    async def get_unread_count(self, user_id: str) -> int:
        r = await self.db.execute(select(func.count()).where(Notification.user_id == user_id, Notification.is_read == False))
        return r.scalar() or 0
    async def mark_read(self, notification_id: str, user_id: str):
        await self.db.execute(update(Notification).where(Notification.id == notification_id, Notification.user_id == user_id).values(is_read=True))
    async def mark_all_read(self, user_id: str):
        await self.db.execute(update(Notification).where(Notification.user_id == user_id).values(is_read=True))
    async def delete(self, notification_id: str, user_id: str):
        n = await self.db.get(Notification, notification_id)
        if n and n.user_id == user_id: n.is_deleted = True
