import csv, io, json
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transaction_repository import TransactionRepository

class ExportService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TransactionRepository(db)
    
    async def export_csv(self, user_id: str, filters: Optional[dict] = None) -> str:
        items, _ = await self.repo.get_by_user(user_id, filters or {}, 1, 10000)
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["date","type","amount","fee","net","status","reference","description"])
        writer.writeheader()
        for t in items:
            writer.writerow({
                "date": t.created_at.isoformat() if t.created_at else "",
                "type": t.transaction_type, "amount": t.amount, "fee": t.fee,
                "net": t.net_amount, "status": t.status, "reference": t.reference or "",
                "description": t.description or "",
            })
        return output.getvalue()
    
    async def export_json(self, user_id: str, filters: Optional[dict] = None) -> str:
        items, _ = await self.repo.get_by_user(user_id, filters or {}, 1, 10000)
        data = [{"date": t.created_at.isoformat() if t.created_at else "", "type": t.transaction_type, "amount": t.amount, "fee": t.fee, "net": t.net_amount, "status": t.status, "reference": t.reference, "description": t.description} for t in items]
        return json.dumps(data, indent=2)
