from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.withdrawal import Withdrawal
router = APIRouter()
@router.post("/{wid}/reject", summary="Reject withdrawal")
async def reject_withdrawal(wid: str, db: AsyncSession = Depends(get_db)):
    w = (await db.execute(select(Withdrawal).where(Withdrawal.id == wid))).scalar_one_or_none()
    if not w: return APIResponse(success=False, message="Not found")
    w.status = "rejected"; await db.commit()
    return APIResponse(success=True, message="Withdrawal rejected")
