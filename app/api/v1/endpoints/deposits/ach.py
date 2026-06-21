from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.deposit_service import DepositService
from app.services.account_service import AccountService
router = APIRouter()

class AchRequest(BaseModel):
    amount: float = Field(..., gt=0)
    account_id: Optional[str] = None
    notes: Optional[str] = None

@router.post("/ach", summary="Ach deposit")
async def ach_deposit(data: AchRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    acct_svc = AccountService(db)
    accounts = await acct_svc.get_user_accounts(user.id)
    acct_id = data.account_id or (accounts["accounts"][0]["id"] if accounts["accounts"] else None)
    if not acct_id: return APIResponse(success=False, message="No account found")
    svc = DepositService(db)
    result = await svc.create_mock_deposit(user.id, acct_id, "ach", data.amount, {"notes": data.notes})
    await db.commit()
    return APIResponse(success=True, message="Ach deposit submitted", data=result)
