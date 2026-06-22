from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user_limit import UserLimit
from sqlalchemy import select
router = APIRouter()

class LimitOverrideRequest(BaseModel):
    daily_deposit_limit: Optional[float] = None; daily_withdrawal_limit: Optional[float] = None
    daily_transfer_limit: Optional[float] = None; per_transaction_limit: Optional[float] = None
    card_spending_limit: Optional[float] = None; atm_withdrawal_limit: Optional[float] = None

@router.put("/{user_id}/limits", summary="Override user limits")
async def update_limits(user_id: str, data: LimitOverrideRequest, db: AsyncSession = Depends(get_db)):
    lim = (await db.execute(select(UserLimit).where(UserLimit.user_id == user_id))).scalar_one_or_none()
    if not lim:
        lim = UserLimit(user_id=user_id); db.add(lim); await db.flush()
    for k, v in data.model_dump(exclude_none=True).items(): setattr(lim, k, v)
    await db.commit()
    return APIResponse(success=True, message="Limits updated")
