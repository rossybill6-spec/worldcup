from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.announcement import Announcement
router = APIRouter()
@router.get("", summary="List announcements")
async def list_announcements(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Announcement).order_by(Announcement.created_at.desc()))).scalars().all()
    data = [{"id":a.id,"title":a.title,"priority":a.priority,"is_published":a.is_published,"created_at":a.created_at.isoformat() if a.created_at else None} for a in rows]
    return APIResponse(success=True, data=data)
