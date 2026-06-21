from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.alert_preference import AlertPreference

class AlertRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def get_preferences(self, user_id: str) -> Optional[AlertPreference]:
        r = await self.db.execute(select(AlertPreference).where(AlertPreference.user_id == user_id))
        return r.scalar_one_or_none()
    async def create_preferences(self, prefs: AlertPreference) -> AlertPreference:
        self.db.add(prefs); await self.db.flush(); return prefs
