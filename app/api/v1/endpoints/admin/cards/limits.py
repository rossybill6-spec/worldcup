from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.card import Card
router = APIRouter()

class CardLimitsRequest(BaseModel):
    daily_spending_limit: Optional[float] = None
    per_transaction_limit: Optional[float] = None
    atm_withdrawal_limit: Optional[float] = None

@router.put("/{card_id}/limits", summary="Set card limits")
async def set_card_limits(card_id: str, data: CardLimitsRequest, db: AsyncSession = Depends(get_db)):
    c = (await db.execute(select(Card).where(Card.id == card_id))).scalar_one_or_none()
    if not c: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(c, k, v)
    await db.commit()
    return APIResponse(success=True, message="Card limits updated")
