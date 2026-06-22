from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
from app.models.user_profile import UserProfile
from sqlalchemy import select, update
router = APIRouter()

class EditUserRequest(BaseModel):
    email: Optional[str] = None; username: Optional[str] = None; phone: Optional[str] = None
    first_name: Optional[str] = None; last_name: Optional[str] = None
    is_active: Optional[bool] = None

@router.put("/{user_id}/edit", summary="Edit user")
async def edit_user(user_id: str, data: EditUserRequest, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    for k, v in data.model_dump(exclude_none=True).items():
        if k in ("first_name", "last_name"):
            p = (await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))).scalar_one_or_none()
            if p: setattr(p, k, v)
        elif hasattr(u, k): setattr(u, k, v)
    await db.commit()
    return APIResponse(success=True, message="User updated")
