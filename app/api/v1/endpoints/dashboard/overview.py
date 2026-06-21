from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.account_service import AccountService
from app.services.transaction_service import TransactionService
from app.services.deposit_service import DepositService
from app.services.withdrawal_service import WithdrawalService
router = APIRouter()

@router.get("/overview", summary="Dashboard overview")
async def overview(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    acct_svc = AccountService(db); accounts = await acct_svc.get_user_accounts(user.id)
    tx_svc = TransactionService(db); recent = await tx_svc.get_recent(user.id, 5)
    return APIResponse(success=True, message="Dashboard overview", data={
        "total_balance": accounts["total_balance"],
        "accounts": accounts["accounts"],
        "recent_transactions": recent,
        "notification_count": 0,
        "pending_deposits": 0,
        "pending_withdrawals": 0,
    })
