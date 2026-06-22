from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
router = APIRouter()

@router.post("/{user_id}/suspend", summary="Suspend user")
async def suspend_user(user_id: str, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    u.is_suspended = True; u.suspended_at = datetime.utcnow()
    await db.commit()
    return APIResponse(success=True, message="User suspended")

@router.post("/{user_id}/activate", summary="Activate user")
async def activate_user(user_id: str, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    u.is_suspended = False; u.is_active = True; u.suspended_at = None
    await db.commit()
    return APIResponse(success=True, message="User activated")
