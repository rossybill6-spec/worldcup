from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transfer import Transfer
from app.models.transfer_template import TransferTemplate

class TransferRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create_transfer(self, t: Transfer) -> Transfer:
        self.db.add(t); await self.db.flush(); return t
    async def get_transfers_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> List[Transfer]:
        r = await self.db.execute(select(Transfer).where(Transfer.user_id == user_id).order_by(Transfer.created_at.desc()).offset(offset).limit(limit))
        return list(r.scalars().all())
    async def create_template(self, t: TransferTemplate) -> TransferTemplate:
        self.db.add(t); await self.db.flush(); return t
    async def get_templates_by_user(self, user_id: str) -> List[TransferTemplate]:
        r = await self.db.execute(select(TransferTemplate).where(TransferTemplate.user_id == user_id, TransferTemplate.is_deleted == False))
        return list(r.scalars().all())
    async def get_template_by_id(self, template_id: str, user_id: str) -> Optional[TransferTemplate]:
        r = await self.db.execute(select(TransferTemplate).where(TransferTemplate.id == template_id, TransferTemplate.user_id == user_id))
        return r.scalar_one_or_none()
    async def delete_template(self, template_id: str, user_id: str) -> bool:
        t = await self.get_template_by_id(template_id, user_id)
        if t: t.is_deleted = True; return True
        return False
