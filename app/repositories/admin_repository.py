from typing import Optional, List
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.admin import Admin
from app.models.admin_session import AdminSession
from app.models.admin_activity_log import AdminActivityLog

class AdminRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def find_by_email(self, email: str) -> Optional[Admin]:
        r = await self.db.execute(select(Admin).where(Admin.email == email, Admin.is_deleted == False))
        return r.scalar_one_or_none()
    async def find_by_id(self, id: str) -> Optional[Admin]:
        r = await self.db.execute(select(Admin).where(Admin.id == id, Admin.is_deleted == False))
        return r.scalar_one_or_none()
    async def create(self, admin: Admin) -> Admin: self.db.add(admin); await self.db.flush(); return admin
    async def get_all(self) -> List[Admin]:
        r = await self.db.execute(select(Admin).where(Admin.is_deleted == False))
        return list(r.scalars().all())
    async def create_session(self, s: AdminSession) -> AdminSession: self.db.add(s); await self.db.flush(); return s
    async def log_activity(self, log: AdminActivityLog): self.db.add(log)
    async def count_users(self) -> int:
        from app.models.user import User
        r = await self.db.execute(select(func.count()).select_from(User).where(User.is_deleted == False))
        return r.scalar() or 0
    async def count_pending_deposits(self) -> int:
        from app.models.deposit import Deposit
        r = await self.db.execute(select(func.count()).select_from(Deposit).where(Deposit.status == "pending"))
        return r.scalar() or 0
    async def count_pending_withdrawals(self) -> int:
        from app.models.withdrawal import Withdrawal
        r = await self.db.execute(select(func.count()).select_from(Withdrawal).where(Withdrawal.status == "pending"))
        return r.scalar() or 0
    async def total_balance(self) -> float:
        from app.models.account import Account
        r = await self.db.execute(select(func.sum(Account.balance)).select_from(Account).where(Account.is_deleted == False))
        return r.scalar() or 0.0
