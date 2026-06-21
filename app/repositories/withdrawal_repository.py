from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.withdrawal import Withdrawal
from app.models.withdrawal_method import WithdrawalMethod

class WithdrawalRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def get_methods(self) -> List[WithdrawalMethod]:
        r = await self.db.execute(select(WithdrawalMethod).where(WithdrawalMethod.is_enabled == True).order_by(WithdrawalMethod.display_order))
        return list(r.scalars().all())
    async def create_withdrawal(self, w: Withdrawal) -> Withdrawal:
        self.db.add(w); await self.db.flush(); return w
    async def get_withdrawals_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Withdrawal]:
        r = await self.db.execute(select(Withdrawal).where(Withdrawal.user_id == user_id).order_by(Withdrawal.created_at.desc()).offset(offset).limit(limit))
        return list(r.scalars().all())
