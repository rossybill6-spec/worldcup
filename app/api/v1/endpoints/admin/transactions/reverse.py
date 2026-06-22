from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.transaction import Transaction
from app.models.account import Account
from sqlalchemy import select
router = APIRouter()

class ReverseRequest(BaseModel): transaction_id: str; reason: str = ""

@router.post("/reverse", summary="Reverse transaction")
async def reverse_tx(data: ReverseRequest, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(Transaction).where(Transaction.id == data.transaction_id, Transaction.status == "completed"))).scalar_one_or_none()
    if not t: return APIResponse(success=False, message="Transaction not found or not completed")
    acct = (await db.execute(select(Account).where(Account.id == t.account_id))).scalar_one_or_none()
    if acct:
        if t.transaction_type.startswith("deposit_"): acct.balance -= t.amount; acct.available_balance -= t.amount
        elif t.transaction_type.startswith("withdrawal_"): acct.balance += t.amount; acct.available_balance += t.amount
        else: acct.balance += t.amount; acct.available_balance += t.amount
    t.status = "reversed"
    await db.commit()
    return APIResponse(success=True, message="Transaction reversed")
