from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_role import AdminRole
from app.models.admin_permission import AdminPermission
from app.constants.permissions import ALL_PERMISSIONS
router = APIRouter()

@router.get("/matrix", summary="Permission matrix (roles x permissions)")
async def permission_matrix(db: AsyncSession = Depends(get_db)):
    roles = (await db.execute(select(AdminRole).where(AdminRole.is_deleted == False))).scalars().all()
    matrix = {}
    for role in roles:
        perms = (await db.execute(select(AdminPermission).where(AdminPermission.role_id == role.id))).scalars().all()
        matrix[role.name] = {k: k in [p.permission_key for p in perms] for k in ALL_PERMISSIONS}
    return APIResponse(success=True, data={"roles": [r.name for r in roles], "permissions": list(ALL_PERMISSIONS.keys()), "matrix": matrix})
