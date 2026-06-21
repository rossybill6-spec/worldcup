from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.card import CardDisputeRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.card_service import CardService
router = APIRouter()
@router.post("/{card_id}/dispute", summary="File a card dispute")
async def file_dispute(card_id: str, data: CardDisputeRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); r = await svc.file_dispute(card_id, user.id, data.transaction_id, data.reason)
    return APIResponse(success=True, message="Dispute filed", data=r)
@router.post("/{card_id}/report-lost", summary="Report card lost/stolen")
async def report_lost(card_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); ok = await svc.report_lost_stolen(card_id, user.id)
    await db.commit(); return APIResponse(success=ok, message="Card reported lost" if ok else "Not found")
