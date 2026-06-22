from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.card import Card
router = APIRouter()
@router.post("/{card_id}/freeze", summary="Admin freeze card")
async def freeze_card(card_id: str, db: AsyncSession = Depends(get_db)):
    c = (await db.execute(select(Card).where(Card.id == card_id))).scalar_one_or_none()
    if not c: return APIResponse(success=False, message="Not found")
    c.is_frozen = True; await db.commit()
    return APIResponse(success=True, message="Card frozen")
@router.post("/{card_id}/cancel", summary="Admin cancel card")
async def cancel_card(card_id: str, db: AsyncSession = Depends(get_db)):
    c = (await db.execute(select(Card).where(Card.id == card_id))).scalar_one_or_none()
    if not c: return APIResponse(success=False, message="Not found")
    c.status = "cancelled"; c.is_frozen = True; await db.commit()
    return APIResponse(success=True, message="Card cancelled")
