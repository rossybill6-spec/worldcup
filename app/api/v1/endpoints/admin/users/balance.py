from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.account import Account
from sqlalchemy import select
router = APIRouter()

class BalanceAdjustRequest(BaseModel):
    account_id: str; amount: float = Field(...); reason: str = ""

@router.post("/{user_id}/balance", summary="Adjust balance")
async def adjust_balance(user_id: str, data: BalanceAdjustRequest, db: AsyncSession = Depends(get_db)):
    a = (await db.execute(select(Account).where(Account.id == data.account_id, Account.user_id == user_id))).scalar_one_or_none()
    if not a: return APIResponse(success=False, message="Account not found")
    a.balance += data.amount; a.available_balance += data.amount
    await db.commit()
    return APIResponse(success=True, message=f"Balance adjusted by \${data.amount:,.2f}")
