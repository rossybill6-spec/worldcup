from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.deposit import Deposit
router = APIRouter()
@router.get("/pending", summary="Pending deposits queue")
async def pending_deposits(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Deposit).where(Deposit.status == "pending").order_by(Deposit.created_at.desc())
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar()
    offset = (page-1)*per_page
    rows = (await db.execute(q.offset(offset).limit(per_page))).scalars().all()
    items = [{"id": d.id, "user_id": d.user_id, "method": d.method, "amount": d.amount, "fee": d.fee, "status": d.status, "reference": d.reference, "created_at": d.created_at.isoformat() if d.created_at else None} for d in rows]
    return APIResponse(success=True, data={"items": items, "total": total, "page": page})
