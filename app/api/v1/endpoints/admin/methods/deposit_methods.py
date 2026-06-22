from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.deposit_method import DepositMethod
router = APIRouter()

class UpdateDepositMethodRequest(BaseModel):
    name: Optional[str] = None; description: Optional[str] = None
    is_enabled: Optional[bool] = None; is_live: Optional[bool] = None
    min_amount: Optional[float] = None; max_amount: Optional[float] = None
    fee_type: Optional[str] = None; fee_amount: Optional[float] = None
    processing_time: Optional[str] = None; instructions: Optional[str] = None
    display_order: Optional[str] = None; requires_admin_approval: Optional[bool] = None

@router.get("/deposit", summary="List deposit methods")
async def list_deposit_methods(db: AsyncSession = Depends(get_db)):
    methods = (await db.execute(select(DepositMethod).order_by(DepositMethod.display_order))).scalars().all()
    data = [{"id":m.id,"name":m.name,"slug":m.slug,"is_enabled":m.is_enabled,"is_live":m.is_live,"min_amount":m.min_amount,"max_amount":m.max_amount,"fee_type":m.fee_type,"fee_amount":m.fee_amount,"processing_time":m.processing_time,"display_order":m.display_order} for m in methods]
    return APIResponse(success=True, data=data)

@router.put("/deposit/{method_id}", summary="Update deposit method")
async def update_deposit_method(method_id: str, data: UpdateDepositMethodRequest, db: AsyncSession = Depends(get_db)):
    m = (await db.execute(select(DepositMethod).where(DepositMethod.id == method_id))).scalar_one_or_none()
    if not m: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(m, k, v)
    await db.commit()
    return APIResponse(success=True, message=f"{m.name} updated")
