from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.bill import MakePaymentRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.bill_service import BillService
router = APIRouter()
@router.post("/pay", summary="Make a bill payment")
async def make_payment(data: MakePaymentRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); r = await svc.make_payment(user.id, data.model_dump())
    if not r.get("success"): return APIResponse(success=False, message=r.get("message","Failed"))
    await db.commit(); return APIResponse(success=True, message="Payment submitted", data=r)
