from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.withdrawal import Withdrawal
from app.models.account import Account
router = APIRouter()
@router.post("/{wid}/approve", summary="Approve withdrawal")
async def approve_withdrawal(wid: str, db: AsyncSession = Depends(get_db)):
    w = (await db.execute(select(Withdrawal).where(Withdrawal.id == wid))).scalar_one_or_none()
    if not w: return APIResponse(success=False, message="Not found")
    w.status = "completed"
    acct = (await db.execute(select(Account).where(Account.id == w.account_id))).scalar_one_or_none()
    if acct: acct.balance -= w.amount; acct.available_balance -= w.amount
    await db.commit()
    return APIResponse(success=True, message="Withdrawal approved")
