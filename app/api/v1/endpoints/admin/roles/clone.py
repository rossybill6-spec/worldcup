from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_role import AdminRole
from app.models.admin_permission import AdminPermission
router = APIRouter()

@router.post("/{role_id}/clone", summary="Clone a role with permissions")
async def clone_role(role_id: str, db: AsyncSession = Depends(get_db)):
    original = (await db.execute(select(AdminRole).where(AdminRole.id == role_id))).scalar_one_or_none()
    if not original: return APIResponse(success=False, message="Not found")
    new_role = AdminRole(name=f"{original.name} (Copy)", description=original.description, level=original.level)
    db.add(new_role); await db.flush()
    perms = (await db.execute(select(AdminPermission).where(AdminPermission.role_id == role_id))).scalars().all()
    for p in perms:
        db.add(AdminPermission(role_id=new_role.id, permission_key=p.permission_key, category=p.category))
    await db.commit()
    return APIResponse(success=True, message=f"Role cloned as {new_role.name}", data={"id": new_role.id})
