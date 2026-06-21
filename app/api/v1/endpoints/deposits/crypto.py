from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.deposit import CryptoDepositInitiateRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.deposit_service import DepositService
from app.services.account_service import AccountService
router = APIRouter()

@router.post("/crypto/initiate", summary="Initiate crypto deposit")
async def initiate_crypto(data: CryptoDepositInitiateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    acct_svc = AccountService(db)
    accounts = await acct_svc.get_user_accounts(user.id)
    checking = next((a for a in accounts["accounts"] if a["account_type"] == "checking"), None)
    if not checking: return APIResponse(success=False, message="No checking account found")
    svc = DepositService(db)
    result = await svc.initiate_crypto_deposit(user.id, checking["id"], data.amount, data.network)
    if not result.get("success"): return APIResponse(success=False, message=result.get("message","Failed"))
    await db.commit()
    return APIResponse(success=True, message="Crypto deposit initiated", data=result)

@router.get("/crypto/session/{reference}", summary="Get crypto deposit session")
async def get_session(reference: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = DepositService(db); session = await svc.repo.get_session_by_reference(reference)
    if not session or session.user_id != user.id: return APIResponse(success=False, message="Session not found")
    return APIResponse(success=True, message="Session found", data={"reference":session.reference,"status":session.status,"network":session.network,"admin_address":session.admin_address})
