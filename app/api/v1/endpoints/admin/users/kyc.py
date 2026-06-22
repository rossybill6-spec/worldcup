from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import select
from datetime import datetime
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
from app.models.user_document import UserDocument
router = APIRouter()

class KYCRequest(BaseModel): status: str; reason: str = ""

@router.put("/{user_id}/kyc", summary="Approve/Reject KYC")
async def update_kyc(user_id: str, data: KYCRequest, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    u.kyc_status = data.status
    if data.status == "approved": u.kyc_verified_at = datetime.utcnow()
    elif data.status == "rejected": u.kyc_rejection_reason = data.reason
    await db.commit()
    return APIResponse(success=True, message=f"KYC {data.status}")
