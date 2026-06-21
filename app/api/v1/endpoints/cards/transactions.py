from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.card_service import CardService
router = APIRouter()
@router.get("/{card_id}/transactions", summary="Get card transactions")
async def get_transactions(card_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); txs = await svc.get_transactions(card_id, user.id)
    return APIResponse(success=True, message="Transactions retrieved", data=txs)
