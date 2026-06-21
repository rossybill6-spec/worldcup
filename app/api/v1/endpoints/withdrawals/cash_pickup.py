from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.withdrawal_service import WithdrawalService
from app.services.account_service import AccountService
router = APIRouter()

class Cash_pickupRequest(BaseModel):
    amount: float = Field(..., gt=0)
    notes: Optional[str] = None

@router.post("/cash_pickup", summary="Cash_pickup withdrawal")
async def cash_pickup_withdrawal(data: Cash_pickupRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    acct_svc = AccountService(db)
    accounts = await acct_svc.get_user_accounts(user.id)
    checking = next((a for a in accounts["accounts"] if a["account_type"] == "checking"), None)
    if not checking: return APIResponse(success=False, message="No checking account found")
    svc = WithdrawalService(db)
    result = await svc.create_withdrawal(user.id, checking["id"], "cash_pickup", data.amount, 0.0, {"notes": data.notes})
    if not result.get("success"): return APIResponse(success=False, message=result.get("message","Failed"))
    await db.commit()
    return APIResponse(success=True, message="Cash_pickup withdrawal submitted", data=result)
