from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.card_service import CardService
router = APIRouter()

class IssueCardRequest(BaseModel): user_id: str; account_id: str; cardholder_name: str

@router.post("/issue", summary="Issue new card to user")
async def issue_card(data: IssueCardRequest, db: AsyncSession = Depends(get_db)):
    svc = CardService(db); card = await svc.create_virtual_card(data.user_id, data.account_id, data.cardholder_name)
    await db.commit()
    return APIResponse(success=True, message="Card issued", data=card)
