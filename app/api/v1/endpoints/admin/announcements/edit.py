from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.announcement import Announcement
router = APIRouter()

class EditAnnouncementRequest(BaseModel):
    title: Optional[str] = None; content: Optional[str] = None
    is_published: Optional[bool] = None; priority: Optional[str] = None

@router.put("/{announcement_id}", summary="Edit announcement")
async def edit_announcement(announcement_id: str, data: EditAnnouncementRequest, db: AsyncSession = Depends(get_db)):
    a = (await db.execute(select(Announcement).where(Announcement.id == announcement_id))).scalar_one_or_none()
    if not a: return APIResponse(success=False, message="Not found")
    for k,v in data.model_dump(exclude_none=True).items(): setattr(a, k, v)
    await db.commit()
    return APIResponse(success=True, message="Announcement updated")
