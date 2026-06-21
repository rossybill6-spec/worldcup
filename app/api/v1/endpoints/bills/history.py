from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.bill_service import BillService
router = APIRouter()
@router.get("/history", summary="Bill payment history")
async def history(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); r = await svc.get_payments(user.id, page, per_page)
    return APIResponse(success=True, message="Payment history", data=r)
