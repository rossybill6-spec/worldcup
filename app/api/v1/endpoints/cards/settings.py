from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.card import CardSettingsRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.card_service import CardService
router = APIRouter()
@router.put("/{card_id}/settings", summary="Update card settings")
async def update_settings(card_id: str, data: CardSettingsRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = CardService(db); ok = await svc.update_settings(card_id, user.id, data.model_dump(exclude_none=True))
    await db.commit(); return APIResponse(success=ok, message="Settings updated" if ok else "Not found")
