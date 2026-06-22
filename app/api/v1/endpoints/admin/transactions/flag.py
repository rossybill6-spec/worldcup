from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.transaction import Transaction
from sqlalchemy import select
router = APIRouter()

class FlagRequest(BaseModel): transaction_id: str; flag: bool = True

@router.post("/flag", summary="Flag/unflag transaction")
async def flag_tx(data: FlagRequest, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(Transaction).where(Transaction.id == data.transaction_id))).scalar_one_or_none()
    if not t: return APIResponse(success=False, message="Not found")
    t.status = "flagged" if data.flag else t.status
    await db.commit()
    return APIResponse(success=True, message="Transaction flagged" if data.flag else "Flag removed")
