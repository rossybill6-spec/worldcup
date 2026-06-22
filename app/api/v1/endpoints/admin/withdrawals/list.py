from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.withdrawal import Withdrawal
router = APIRouter()
@router.get("/list", summary="All withdrawals")
async def list_withdrawals(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), status: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    q = select(Withdrawal).order_by(Withdrawal.created_at.desc())
    if status: q = q.where(Withdrawal.status == status)
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar()
    offset = (page-1)*per_page
    rows = (await db.execute(q.offset(offset).limit(per_page))).scalars().all()
    items = [{"id": w.id, "user_id": w.user_id, "method": w.method, "amount": w.amount, "status": w.status, "reference": w.reference, "created_at": w.created_at.isoformat() if w.created_at else None} for w in rows]
    return APIResponse(success=True, data={"items": items, "total": total})
