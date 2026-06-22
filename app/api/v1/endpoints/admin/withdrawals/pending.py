from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.withdrawal import Withdrawal
router = APIRouter()
@router.get("/pending", summary="Pending withdrawals")
async def pending_withdrawals(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Withdrawal).where(Withdrawal.status == "pending").order_by(Withdrawal.created_at.desc())
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar()
    offset = (page-1)*per_page
    rows = (await db.execute(q.offset(offset).limit(per_page))).scalars().all()
    items = [{"id": w.id, "user_id": w.user_id, "method": w.method, "amount": w.amount, "fee": w.fee, "status": w.status, "reference": w.reference, "created_at": w.created_at.isoformat() if w.created_at else None} for w in rows]
    return APIResponse(success=True, data={"items": items, "total": total})
