from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.alert_repository import AlertRepository
from app.models.alert_preference import AlertPreference

class AlertService:
    def __init__(self, db: AsyncSession): self.db = db; self.repo = AlertRepository(db)
    
    async def get_preferences(self, user_id: str) -> Dict:
        prefs = await self.repo.get_preferences(user_id)
        if not prefs:
            prefs = AlertPreference(user_id=user_id)
            await self.repo.create_preferences(prefs)
            await self.db.flush()
        return {"balance_low": prefs.balance_low, "balance_low_threshold": prefs.balance_low_threshold,
                "balance_high": prefs.balance_high, "balance_high_threshold": prefs.balance_high_threshold,
                "large_deposit": prefs.large_deposit, "large_deposit_threshold": prefs.large_deposit_threshold,
                "large_withdrawal": prefs.large_withdrawal, "large_withdrawal_threshold": prefs.large_withdrawal_threshold,
                "security_login": prefs.security_login, "security_password_change": prefs.security_password_change,
                "weekly_summary": prefs.weekly_summary, "monthly_summary": prefs.monthly_summary}
    
    async def update_preferences(self, user_id: str, data: dict) -> bool:
        prefs = await self.repo.get_preferences(user_id)
        if not prefs:
            prefs = AlertPreference(user_id=user_id)
            await self.repo.create_preferences(prefs)
        for k, v in data.items():
            if v is not None: setattr(prefs, k, v)
        return True
