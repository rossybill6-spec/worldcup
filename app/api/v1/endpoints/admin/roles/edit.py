from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_role import AdminRole
router = APIRouter()

class EditRoleRequest(BaseModel):
    name: Optional[str] = None; description: Optional[str] = None; level: Optional[str] = None

@router.put("/{role_id}", summary="Edit role")
async def edit_role(role_id: str, data: EditRoleRequest, db: AsyncSession = Depends(get_db)):
    r = (await db.execute(select(AdminRole).where(AdminRole.id == role_id))).scalar_one_or_none()
    if not r: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(r, k, v)
    await db.commit()
    return APIResponse(success=True, message="Role updated")
