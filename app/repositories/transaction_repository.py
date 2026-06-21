from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, and_, or_, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction

class TransactionRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create(self, t: Transaction) -> Transaction: self.db.add(t); await self.db.flush(); return t
    async def get_by_user(self, user_id: str, filters: dict = None, page: int = 1, per_page: int = 20) -> tuple:
        q = select(Transaction).where(Transaction.user_id == user_id)
        if filters:
            if filters.get("transaction_type"): q = q.where(Transaction.transaction_type == filters["transaction_type"])
            if filters.get("status"): q = q.where(Transaction.status == filters["status"])
            if filters.get("start_date"): q = q.where(Transaction.created_at >= datetime.fromisoformat(filters["start_date"]))
            if filters.get("end_date"): q = q.where(Transaction.created_at <= datetime.fromisoformat(filters["end_date"]))
            if filters.get("min_amount"): q = q.where(Transaction.amount >= filters["min_amount"])
            if filters.get("max_amount"): q = q.where(Transaction.amount <= filters["max_amount"])
            if filters.get("search"):
                s = f"%{filters['search']}%"
                q = q.where(or_(Transaction.description.ilike(s), Transaction.reference.ilike(s), Transaction.recipient.ilike(s)))
        sort_col = getattr(Transaction, filters.get("sort_by", "created_at"), Transaction.created_at)
        q = q.order_by(desc(sort_col) if filters.get("sort_order")=="desc" else asc(sort_col))
        count_q = select(func.count()).select_from(q.subquery())
        total = (await self.db.execute(count_q)).scalar()
        offset = (page-1)*per_page
        r = await self.db.execute(q.offset(offset).limit(per_page))
        return list(r.scalars().all()), total
    async def get_recent(self, user_id: str, limit: int = 10) -> List[Transaction]:
        r = await self.db.execute(select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.created_at.desc()).limit(limit))
        return list(r.scalars().all())
