from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.transaction import Transaction
from app.models.deposit import Deposit
from app.models.withdrawal import Withdrawal
from sqlalchemy import select
router = APIRouter()

class RejectRequest(BaseModel): transaction_id: str; reason: str = ""

@router.post("/reject", summary="Reject transaction")
async def reject_tx(data: RejectRequest, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(Transaction).where(Transaction.id == data.transaction_id))).scalar_one_or_none()
    if not t: return APIResponse(success=False, message="Transaction not found")
    if t.transaction_type.startswith("deposit_"):
        dep = (await db.execute(select(Deposit).where(Deposit.reference == t.reference))).scalar_one_or_none()
        if dep: dep.status = "rejected"; dep.admin_notes = data.reason
    elif t.transaction_type.startswith("withdrawal_"):
        wth = (await db.execute(select(Withdrawal).where(Withdrawal.reference == t.reference))).scalar_one_or_none()
        if wth: wth.status = "rejected"; wth.admin_notes = data.reason
    t.status = "rejected"
    await db.commit()
    return APIResponse(success=True, message="Transaction rejected")
