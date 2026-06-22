from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.interest import UpdateInterestRequest
from app.schemas.common import APIResponse
from app.models.interest_rate import InterestRate
router = APIRouter()

@router.get("/list", summary="List interest rates")
async def list_rates(db: AsyncSession = Depends(get_db)):
    rates = (await db.execute(select(InterestRate).order_by(InterestRate.account_type))).scalars().all()
    data = [{"id":r.id,"account_type":r.account_type,"rate":r.rate,"min_balance":r.min_balance,"max_balance":r.max_balance,"is_enabled":r.is_enabled} for r in rates]
    return APIResponse(success=True, data=data)

@router.put("/{rate_id}", summary="Update interest rate")
async def update_rate(rate_id: str, data: UpdateInterestRequest, db: AsyncSession = Depends(get_db)):
    r = (await db.execute(select(InterestRate).where(InterestRate.id == rate_id))).scalar_one_or_none()
    if not r: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(r, k, v)
    await db.commit()
    return APIResponse(success=True, message="Rate updated")
