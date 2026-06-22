from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.deposit import Deposit
router = APIRouter()
@router.get("/list", summary="All deposits")
async def list_deposits(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    q = select(Deposit).order_by(Deposit.created_at.desc())
    if status: q = q.where(Deposit.status == status)
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar()
    offset = (page-1)*per_page
    rows = (await db.execute(q.offset(offset).limit(per_page))).scalars().all()
    items = [{"id": d.id, "user_id": d.user_id, "method": d.method, "amount": d.amount, "status": d.status, "reference": d.reference, "created_at": d.created_at.isoformat() if d.created_at else None} for d in rows]
    return APIResponse(success=True, data={"items": items, "total": total})
