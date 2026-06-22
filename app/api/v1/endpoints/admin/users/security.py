from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
from app.utils.hashers import hash_user_password
router = APIRouter()

@router.post("/{user_id}/reset-password", summary="Reset user password")
async def reset_password(user_id: str, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    u.password_hash = hash_user_password("TempPass123!")
    await db.commit()
    return APIResponse(success=True, message="Password reset to TempPass123!")

@router.post("/{user_id}/reset-2fa", summary="Reset user 2FA")
async def reset_2fa(user_id: str, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    u.is_2fa_enabled = False; u.two_fa_secret = None; await db.commit()
    return APIResponse(success=True, message="2FA reset")
