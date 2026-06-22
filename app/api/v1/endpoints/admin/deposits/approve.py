from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.deposit import Deposit
from app.models.account import Account
router = APIRouter()
@router.post("/{deposit_id}/approve", summary="Approve deposit")
async def approve_deposit(deposit_id: str, db: AsyncSession = Depends(get_db)):
    d = (await db.execute(select(Deposit).where(Deposit.id == deposit_id))).scalar_one_or_none()
    if not d: return APIResponse(success=False, message="Not found")
    d.status = "completed"
    acct = (await db.execute(select(Account).where(Account.id == d.account_id))).scalar_one_or_none()
    if acct: acct.balance += d.amount; acct.available_balance += d.amount
    await db.commit()
    return APIResponse(success=True, message="Deposit approved")
