from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin import Admin
router = APIRouter()
@router.get("/list", summary="List all admins")
async def list_admins(db: AsyncSession = Depends(get_db)):
    admins = (await db.execute(select(Admin).where(Admin.is_deleted == False))).scalars().all()
    data = [{"id":a.id,"email":a.email,"username":a.username,"full_name":a.full_name,"is_active":a.is_active,"is_super_admin":a.is_super_admin,"last_login_at":a.last_login_at.isoformat() if a.last_login_at else None} for a in admins]
    return APIResponse(success=True, data=data)
