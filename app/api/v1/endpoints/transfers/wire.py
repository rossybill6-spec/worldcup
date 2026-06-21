from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.transfer import WireTransferRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.transfer_service import TransferService
router = APIRouter()
@router.post("/wire", summary="Wire transfer")
async def wire_transfer(data: WireTransferRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = TransferService(db); r = await svc.wire_transfer(user.id, data.from_account_id, data.amount, data.recipient_name, data.recipient_account, data.recipient_routing, data.recipient_bank, data.swift_code, data.recipient_address, data.memo)
    if not r.get("success"): return APIResponse(success=False, message=r.get("message","Failed"))
    await db.commit()
    return APIResponse(success=True, message="Wire transfer submitted", data=r)
