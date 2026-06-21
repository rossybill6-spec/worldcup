from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.card import ActivateCardRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.card_service import CardService
router = APIRouter()
@router.post("/{card_id}/request-physical", summary="Request physical card")
async def request_physical(card_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); ok = await svc.request_physical(card_id, user.id)
    await db.commit(); return APIResponse(success=ok, message="Physical card requested" if ok else "Not found")
@router.post("/{card_id}/activate", summary="Activate physical card")
async def activate(card_id: str, data: ActivateCardRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); ok = await svc.activate_physical(card_id, user.id, data.last_four)
    await db.commit(); return APIResponse(success=ok, message="Card activated" if ok else "Activation failed")
