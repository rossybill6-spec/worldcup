from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_activity_log import AdminActivityLog
router = APIRouter()
@router.get("/activity/{admin_id}", summary="Get admin activity log")
async def admin_activity(admin_id: str, db: AsyncSession = Depends(get_db)):
    logs = (await db.execute(select(AdminActivityLog).where(AdminActivityLog.admin_id == admin_id).order_by(AdminActivityLog.created_at.desc()).limit(50))).scalars().all()
    data = [{"action":l.action,"target_type":l.target_type,"target_id":l.target_id,"details":l.details,"ip_address":l.ip_address,"created_at":l.created_at.isoformat() if l.created_at else None} for l in logs]
    return APIResponse(success=True, data=data)
