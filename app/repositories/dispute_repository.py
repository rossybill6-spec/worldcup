from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction_dispute import TransactionDispute

class DisputeRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create(self, d: TransactionDispute) -> TransactionDispute: self.db.add(d); await self.db.flush(); return d
