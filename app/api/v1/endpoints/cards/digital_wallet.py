from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.card import DigitalWalletRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.card_service import CardService
router = APIRouter()
@router.post("/{card_id}/digital-wallet", summary="Add to digital wallet")
async def add_digital_wallet(card_id: str, data: DigitalWalletRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); ok = await svc.setup_digital_wallet(card_id, user.id, data.wallet_type)
    await db.commit(); return APIResponse(success=ok, message=f"Added to {data.wallet_type}" if ok else "Not found")
