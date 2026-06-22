from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.transaction import Transaction
from app.models.deposit import Deposit
from app.models.withdrawal import Withdrawal
from app.models.account import Account
from sqlalchemy import select
router = APIRouter()

class ApproveRequest(BaseModel): transaction_id: str; notes: str = ""

@router.post("/approve", summary="Approve transaction")
async def approve_tx(data: ApproveRequest, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(Transaction).where(Transaction.id == data.transaction_id))).scalar_one_or_none()
    if not t: return APIResponse(success=False, message="Transaction not found")
    if t.transaction_type.startswith("deposit_"):
        dep = (await db.execute(select(Deposit).where(Deposit.reference == t.reference))).scalar_one_or_none()
        if dep:
            dep.status = "completed"; dep.admin_notes = data.notes
            acct = (await db.execute(select(Account).where(Account.id == t.account_id))).scalar_one_or_none()
            if acct: acct.balance += t.amount; acct.available_balance += t.amount
    elif t.transaction_type.startswith("withdrawal_"):
        wth = (await db.execute(select(Withdrawal).where(Withdrawal.reference == t.reference))).scalar_one_or_none()
        if wth:
            wth.status = "completed"; wth.admin_notes = data.notes
            acct = (await db.execute(select(Account).where(Account.id == t.account_id))).scalar_one_or_none()
            if acct: acct.balance -= t.amount; acct.available_balance -= t.amount
    t.status = "completed"
    await db.commit()
    return APIResponse(success=True, message="Transaction approved")
