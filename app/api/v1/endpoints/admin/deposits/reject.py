from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.deposit import Deposit
router = APIRouter()
@router.post("/{deposit_id}/reject", summary="Reject deposit")
async def reject_deposit(deposit_id: str, db: AsyncSession = Depends(get_db)):
    d = (await db.execute(select(Deposit).where(Deposit.id == deposit_id))).scalar_one_or_none()
    if not d: return APIResponse(success=False, message="Not found")
    d.status = "rejected"; await db.commit()
    return APIResponse(success=True, message="Deposit rejected")
