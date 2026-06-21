from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.transaction_service import TransactionService
router = APIRouter()

@router.get("/all", summary="All transactions (unified)")
async def all_transactions(
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    transaction_type: Optional[str] = None, status: Optional[str] = None,
    start_date: Optional[str] = None, end_date: Optional[str] = None,
    search: Optional[str] = None, sort_by: str = "created_at", sort_order: str = "desc",
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
):
    filters = {k:v for k,v in {"transaction_type":transaction_type,"status":status,"start_date":start_date,"end_date":end_date,"search":search,"sort_by":sort_by,"sort_order":sort_order}.items() if v is not None}
    svc = TransactionService(db); result = await svc.get_history(user.id, filters, page, per_page)
    return APIResponse(success=True, message="Transactions retrieved", data=result)
