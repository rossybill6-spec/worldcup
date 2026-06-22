from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.notification import Notification
router = APIRouter()
@router.get("", summary="Notification history")
async def history(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Notification).order_by(Notification.created_at.desc()).offset((page-1)*per_page).limit(per_page)
    rows = (await db.execute(q)).scalars().all()
    data = [{"id":n.id,"title":n.title,"notification_type":n.notification_type,"is_read":n.is_read,"created_at":n.created_at.isoformat() if n.created_at else None} for n in rows]
    return APIResponse(success=True, data=data)
