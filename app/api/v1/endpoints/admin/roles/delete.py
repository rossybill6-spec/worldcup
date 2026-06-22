from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_role import AdminRole
router = APIRouter()
@router.delete("/{role_id}", summary="Delete role")
async def delete_role(role_id: str, db: AsyncSession = Depends(get_db)):
    r = (await db.execute(select(AdminRole).where(AdminRole.id == role_id, AdminRole.is_system == "false"))).scalar_one_or_none()
    if not r: return APIResponse(success=False, message="Cannot delete system role or not found")
    r.is_deleted = True; await db.commit()
    return APIResponse(success=True, message="Role deleted")
