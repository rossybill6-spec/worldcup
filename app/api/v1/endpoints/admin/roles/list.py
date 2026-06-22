from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_role import AdminRole
router = APIRouter()

@router.get("/list", summary="List all roles")
async def list_roles(db: AsyncSession = Depends(get_db)):
    roles = (await db.execute(select(AdminRole).where(AdminRole.is_deleted == False))).scalars().all()
    data = [{"id":r.id,"name":r.name,"description":r.description,"level":r.level,"is_system":r.is_system,"created_at":r.created_at.isoformat() if r.created_at else None} for r in roles]
    return APIResponse(success=True, data=data)
