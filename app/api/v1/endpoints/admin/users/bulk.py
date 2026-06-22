from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
from app.models.user_tag import UserTag
from sqlalchemy import select
router = APIRouter()

class BulkRequest(BaseModel): user_ids: List[str]; action: str; value: str = ""

@router.post("/bulk", summary="Bulk user operations")
async def bulk_operation(data: BulkRequest, db: AsyncSession = Depends(get_db)):
    for uid in data.user_ids:
        u = (await db.execute(select(User).where(User.id == uid))).scalar_one_or_none()
        if not u: continue
        if data.action == "suspend": u.is_suspended = True
        elif data.action == "activate": u.is_suspended = False; u.is_active = True
        elif data.action == "tag": db.add(UserTag(user_id=uid, tag=data.value))
        elif data.action == "delete": u.is_deleted = True; u.is_active = False
    await db.commit()
    return APIResponse(success=True, message=f"Bulk {data.action} completed for {len(data.user_ids)} users")
