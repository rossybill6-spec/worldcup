from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.fee_schedule import FeeSchedule
router = APIRouter()

class CreateFeeRequest(BaseModel):
    name: str = Field(..., min_length=2); slug: str; amount: float = 0.0
    fee_type: str = "flat"; category: Optional[str] = None; description: Optional[str] = None

@router.post("/create", summary="Add new fee")
async def create_fee(data: CreateFeeRequest, db: AsyncSession = Depends(get_db)):
    fee = FeeSchedule(**data.model_dump())
    db.add(fee); await db.commit()
    return APIResponse(success=True, message="Fee created", data={"id": fee.id})
