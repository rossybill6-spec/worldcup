from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user_session import UserSession
router = APIRouter()

@router.post("/{user_id}/force-logout", summary="Force logout user")
async def force_logout(user_id: str, db: AsyncSession = Depends(get_db)):
    await db.execute(update(UserSession).where(UserSession.user_id == user_id, UserSession.is_active == True).values(is_active=False, logged_out_at=datetime.utcnow()))
    await db.commit()
    return APIResponse(success=True, message="All sessions terminated")
