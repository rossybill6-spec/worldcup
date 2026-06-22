from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.fee_schedule import FeeSchedule
router = APIRouter()
@router.get("/list", summary="List all fees")
async def list_fees(db: AsyncSession = Depends(get_db)):
    fees = (await db.execute(select(FeeSchedule).order_by(FeeSchedule.category, FeeSchedule.name))).scalars().all()
    data = [{"id":f.id,"name":f.name,"slug":f.slug,"amount":f.amount,"fee_type":f.fee_type,"is_enabled":f.is_enabled,"category":f.category,"description":f.description} for f in fees]
    return APIResponse(success=True, data=data)
