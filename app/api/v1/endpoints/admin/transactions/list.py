from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.transaction import Transaction
router = APIRouter()

@router.get("/list", summary="All transactions")
async def list_transactions(
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    transaction_type: Optional[str] = None, status: Optional[str] = None,
    search: Optional[str] = None, user_id: Optional[str] = None,
    start_date: Optional[str] = None, end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Transaction).where(Transaction.is_deleted == False)
    if transaction_type: q = q.where(Transaction.transaction_type == transaction_type)
    if status: q = q.where(Transaction.status == status)
    if user_id: q = q.where(Transaction.user_id == user_id)
    if search: q = q.where(or_(Transaction.description.ilike(f"%{search}%"), Transaction.reference.ilike(f"%{search}%")))
    if start_date: q = q.where(Transaction.created_at >= start_date)
    if end_date: q = q.where(Transaction.created_at <= end_date)
    q = q.order_by(Transaction.created_at.desc())
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar()
    offset = (page-1)*per_page
    rows = (await db.execute(q.offset(offset).limit(per_page))).scalars().all()
    items = [{"id": t.id, "transaction_type": t.transaction_type, "amount": t.amount, "fee": t.fee, "net_amount": t.net_amount, "status": t.status, "reference": t.reference, "description": t.description, "user_id": t.user_id, "created_at": t.created_at.isoformat() if t.created_at else None} for t in rows]
    return APIResponse(success=True, data={"items": items, "total": total, "page": page, "per_page": per_page})
