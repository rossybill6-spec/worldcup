from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.bill_payee import BillPayee
from app.models.bill_payment import BillPayment
from app.models.bill_schedule import BillSchedule

class BillRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create_payee(self, p: BillPayee) -> BillPayee: self.db.add(p); await self.db.flush(); return p
    async def get_payees(self, user_id: str) -> List[BillPayee]:
        r = await self.db.execute(select(BillPayee).where(BillPayee.user_id == user_id, BillPayee.is_deleted == False))
        return list(r.scalars().all())
    async def get_payee(self, payee_id: str, user_id: str) -> Optional[BillPayee]:
        r = await self.db.execute(select(BillPayee).where(BillPayee.id == payee_id, BillPayee.user_id == user_id))
        return r.scalar_one_or_none()
    async def delete_payee(self, payee_id: str, user_id: str) -> bool:
        p = await self.get_payee(payee_id, user_id)
        if p: p.is_deleted = True; return True
        return False
    async def create_payment(self, pmt: BillPayment) -> BillPayment: self.db.add(pmt); await self.db.flush(); return pmt
    async def get_payments(self, user_id: str, limit: int = 20, offset: int = 0) -> List[BillPayment]:
        r = await self.db.execute(select(BillPayment).where(BillPayment.user_id == user_id).order_by(BillPayment.created_at.desc()).offset(offset).limit(limit))
        return list(r.scalars().all())
    async def create_schedule(self, s: BillSchedule) -> BillSchedule: self.db.add(s); await self.db.flush(); return s
    async def get_schedules(self, user_id: str) -> List[BillSchedule]:
        r = await self.db.execute(select(BillSchedule).where(BillSchedule.user_id == user_id, BillSchedule.is_deleted == False))
        return list(r.scalars().all())
    async def get_schedule(self, schedule_id: str, user_id: str) -> Optional[BillSchedule]:
        r = await self.db.execute(select(BillSchedule).where(BillSchedule.id == schedule_id, BillSchedule.user_id == user_id))
        return r.scalar_one_or_none()
    async def delete_schedule(self, schedule_id: str, user_id: str) -> bool:
        s = await self.get_schedule(schedule_id, user_id)
        if s: s.is_deleted = True; return True
        return False
