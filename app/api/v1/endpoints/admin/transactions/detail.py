from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.transaction import Transaction
router = APIRouter()
@router.get("/{tx_id}", summary="Transaction detail")
async def tx_detail(tx_id: str, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(Transaction).where(Transaction.id == tx_id))).scalar_one_or_none()
    if not t: return APIResponse(success=False, message="Not found")
    return APIResponse(success=True, data={"id": t.id, "transaction_type": t.transaction_type, "amount": t.amount, "fee": t.fee, "net_amount": t.net_amount, "status": t.status, "reference": t.reference, "description": t.description, "source": t.source, "recipient": t.recipient, "user_id": t.user_id, "account_id": t.account_id, "created_at": t.created_at.isoformat() if t.created_at else None})
