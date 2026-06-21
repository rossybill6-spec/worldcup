"""Deposit repository."""
from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.deposit import Deposit
from app.models.deposit_method import DepositMethod
from app.models.deposit_session import DepositSession

class DepositRepository:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def get_methods(self) -> List[DepositMethod]:
        r = await self.db.execute(select(DepositMethod).where(DepositMethod.is_enabled == True).order_by(DepositMethod.display_order))
        return list(r.scalars().all())
    
    async def get_method_by_slug(self, slug: str) -> Optional[DepositMethod]:
        r = await self.db.execute(select(DepositMethod).where(DepositMethod.slug == slug))
        return r.scalar_one_or_none()
    
    async def create_deposit(self, deposit: Deposit) -> Deposit:
        self.db.add(deposit); await self.db.flush(); return deposit
    
    async def create_session(self, session: DepositSession) -> DepositSession:
        self.db.add(session); await self.db.flush(); return session
    
    async def get_deposits_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Deposit]:
        r = await self.db.execute(select(Deposit).where(Deposit.user_id == user_id).order_by(Deposit.created_at.desc()).offset(offset).limit(limit))
        return list(r.scalars().all())
    
    async def get_deposit_by_reference(self, reference: str) -> Optional[Deposit]:
        r = await self.db.execute(select(Deposit).where(Deposit.reference == reference))
        return r.scalar_one_or_none()
    
    async def get_session_by_reference(self, reference: str) -> Optional[DepositSession]:
        r = await self.db.execute(select(DepositSession).where(DepositSession.reference == reference))
        return r.scalar_one_or_none()
