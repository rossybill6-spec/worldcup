from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin import Admin
router = APIRouter()

class ChangeRoleRequest(BaseModel): role_id: str

@router.put("/{admin_id}/role", summary="Change admin role")
async def change_role(admin_id: str, data: ChangeRoleRequest, db: AsyncSession = Depends(get_db)):
    a = (await db.execute(select(Admin).where(Admin.id == admin_id))).scalar_one_or_none()
    if not a: return APIResponse(success=False, message="Not found")
    a.role_id = data.role_id; await db.commit()
    return APIResponse(success=True, message="Role updated")
