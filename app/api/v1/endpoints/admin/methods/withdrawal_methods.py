from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.withdrawal_method import WithdrawalMethod
router = APIRouter()

class UpdateWithdrawalMethodRequest(BaseModel):
    name: Optional[str] = None; is_enabled: Optional[bool] = None
    min_amount: Optional[float] = None; max_amount: Optional[float] = None
    fee_type: Optional[str] = None; fee_amount: Optional[float] = None
    processing_time: Optional[str] = None; display_order: Optional[str] = None

@router.get("/withdrawal", summary="List withdrawal methods")
async def list_withdrawal_methods(db: AsyncSession = Depends(get_db)):
    methods = (await db.execute(select(WithdrawalMethod).order_by(WithdrawalMethod.display_order))).scalars().all()
    data = [{"id":m.id,"name":m.name,"slug":m.slug,"is_enabled":m.is_enabled,"min_amount":m.min_amount,"max_amount":m.max_amount,"fee_amount":m.fee_amount,"processing_time":m.processing_time} for m in methods]
    return APIResponse(success=True, data=data)

@router.put("/withdrawal/{method_id}", summary="Update withdrawal method")
async def update_withdrawal_method(method_id: str, data: UpdateWithdrawalMethodRequest, db: AsyncSession = Depends(get_db)):
    m = (await db.execute(select(WithdrawalMethod).where(WithdrawalMethod.id == method_id))).scalar_one_or_none()
    if not m: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(m, k, v)
    await db.commit()
    return APIResponse(success=True, message=f"{m.name} updated")
