from typing import Dict, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository
from app.repositories.dispute_repository import DisputeRepository
from app.models.transaction import Transaction
from app.models.transaction_dispute import TransactionDispute

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db; self.repo = TransactionRepository(db); self.acct_repo = AccountRepository(db); self.dispute_repo = DisputeRepository(db)
    
    async def record(self, user_id: str, account_id: str, tx_type: str, amount: float, status: str = "completed", reference: str = None, description: str = None, source: str = None, recipient: str = None, fee: float = 0.0) -> Transaction:
        t = Transaction(user_id=user_id, account_id=account_id, transaction_type=tx_type, amount=amount, fee=fee, net_amount=amount-fee, currency="USD", status=status, reference=reference, description=description, source=source, recipient=recipient, created_at=datetime.utcnow())
        return await self.repo.create(t)
    
    async def get_history(self, user_id: str, filters: dict = None, page: int = 1, per_page: int = 20) -> Dict:
        items, total = await self.repo.get_by_user(user_id, filters, page, per_page)
        data = [{"id": t.id, "transaction_type": t.transaction_type, "amount": t.amount, "fee": t.fee, "net_amount": t.net_amount, "currency": t.currency, "status": t.status, "reference": t.reference, "description": t.description, "source": t.source, "recipient": t.recipient, "category": t.category, "created_at": t.created_at.isoformat() if t.created_at else None} for t in items]
        return {"items": data, "total": total, "page": page, "per_page": per_page, "total_pages": (total + per_page - 1) // per_page}
    
    async def get_recent(self, user_id: str, limit: int = 10) -> List:
        txs = await self.repo.get_recent(user_id, limit)
        return [{"id": t.id, "transaction_type": t.transaction_type, "amount": t.amount, "status": t.status, "reference": t.reference, "description": t.description, "created_at": t.created_at.isoformat() if t.created_at else None} for t in txs]
    
    async def file_dispute(self, user_id: str, transaction_id: str, reason: str) -> Dict:
        d = TransactionDispute(user_id=user_id, transaction_id=transaction_id, reason=reason)
        await self.dispute_repo.create(d)
        return {"success": True, "dispute_id": d.id, "status": "open"}
