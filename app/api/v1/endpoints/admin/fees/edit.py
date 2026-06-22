from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.fee import UpdateFeeRequest
from app.schemas.common import APIResponse
from app.models.fee_schedule import FeeSchedule
router = APIRouter()
@router.put("/{fee_id}", summary="Update fee")
async def update_fee(fee_id: str, data: UpdateFeeRequest, db: AsyncSession = Depends(get_db)):
    f = (await db.execute(select(FeeSchedule).where(FeeSchedule.id == fee_id))).scalar_one_or_none()
    if not f: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(f, k, v)
    await db.commit()
    return APIResponse(success=True, message=f"{f.name} updated")
