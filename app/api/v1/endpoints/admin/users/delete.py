from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
router = APIRouter()
@router.delete("/{user_id}", summary="Delete user")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    u.is_deleted = True; u.is_active = False; u.deleted_at = datetime.utcnow()
    await db.commit()
    return APIResponse(success=True, message="User deleted")
