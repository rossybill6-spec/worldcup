from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_permission import AdminPermission
router = APIRouter()

class AssignPermissionsRequest(BaseModel):
    permissions: List[str]

@router.get("/{role_id}/permissions", summary="Get role permissions")
async def get_permissions(role_id: str, db: AsyncSession = Depends(get_db)):
    perms = (await db.execute(select(AdminPermission).where(AdminPermission.role_id == role_id))).scalars().all()
    return APIResponse(success=True, data=[p.permission_key for p in perms])

@router.put("/{role_id}/permissions", summary="Assign permissions to role")
async def assign_permissions(role_id: str, data: AssignPermissionsRequest, db: AsyncSession = Depends(get_db)):
    old = (await db.execute(select(AdminPermission).where(AdminPermission.role_id == role_id))).scalars().all()
    for p in old: p.is_deleted = True
    for key in data.permissions:
        db.add(AdminPermission(role_id=role_id, permission_key=key))
    await db.commit()
    return APIResponse(success=True, message=f"{len(data.permissions)} permissions assigned")
