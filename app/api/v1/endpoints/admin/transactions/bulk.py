from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.transaction import Transaction
from app.models.deposit import Deposit
from app.models.account import Account
from sqlalchemy import select
router = APIRouter()

class BulkTxRequest(BaseModel): transaction_ids: List[str]; action: str

@router.post("/bulk", summary="Bulk approve/reject")
async def bulk_tx(data: BulkTxRequest, db: AsyncSession = Depends(get_db)):
    for tid in data.transaction_ids:
        t = (await db.execute(select(Transaction).where(Transaction.id == tid))).scalar_one_or_none()
        if not t: continue
        if data.action == "approve" and t.transaction_type.startswith("deposit_"):
            dep = (await db.execute(select(Deposit).where(Deposit.reference == t.reference))).scalar_one_or_none()
            if dep:
                dep.status = "completed"
                acct = (await db.execute(select(Account).where(Account.id == t.account_id))).scalar_one_or_none()
                if acct: acct.balance += t.amount; acct.available_balance += t.amount
            t.status = "completed"
        elif data.action == "reject":
            t.status = "rejected"
            dep = (await db.execute(select(Deposit).where(Deposit.reference == t.reference))).scalar_one_or_none()
            if dep: dep.status = "rejected"
    await db.commit()
    return APIResponse(success=True, message=f"Bulk {data.action} completed")
