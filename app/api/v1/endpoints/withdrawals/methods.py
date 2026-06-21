from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.withdrawal_service import WithdrawalService
router = APIRouter()
@router.get("/methods", summary="List withdrawal methods")
async def list_methods(db: AsyncSession = Depends(get_db)):
    svc = WithdrawalService(db); methods = await svc.get_methods()
    return APIResponse(success=True, message="Withdrawal methods", data=methods)
