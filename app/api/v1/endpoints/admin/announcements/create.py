from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.announcement import Announcement
router = APIRouter()

class CreateAnnouncementRequest(BaseModel):
    title: str = Field(...); content: str = Field(...); priority: str = "normal"

@router.post("", summary="Create announcement")
async def create_announcement(data: CreateAnnouncementRequest, db: AsyncSession = Depends(get_db)):
    a = Announcement(title=data.title, content=data.content, priority=data.priority, is_published=True)
    db.add(a); await db.commit()
    return APIResponse(success=True, message="Announcement created", data={"id":a.id})
