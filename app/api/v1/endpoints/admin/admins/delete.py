from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin import Admin
router = APIRouter()
@router.delete("/{admin_id}", summary="Delete admin")
async def delete_admin(admin_id: str, db: AsyncSession = Depends(get_db)):
    a = (await db.execute(select(Admin).where(Admin.id == admin_id, Admin.is_super_admin == False))).scalar_one_or_none()
    if not a: return APIResponse(success=False, message="Cannot delete super admin or not found")
    a.is_deleted = True; await db.commit()
    return APIResponse(success=True, message="Admin deleted")
