from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.deposit_service import DepositService
router = APIRouter()
@router.get("/methods", summary="List deposit methods")
async def list_methods(db: AsyncSession = Depends(get_db)):
    svc = DepositService(db); methods = await svc.get_methods()
    return APIResponse(success=True, message="Deposit methods", data=methods)
