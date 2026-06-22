from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.admin_permission import AdminPermission

class PermissionRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def get_by_role(self, role_id: str) -> List[AdminPermission]:
        r = await self.db.execute(select(AdminPermission).where(AdminPermission.role_id == role_id))
        return list(r.scalars().all())
    async def assign(self, role_id: str, permissions: List[str]):
        await self.db.execute(select(AdminPermission).where(AdminPermission.role_id == role_id))
        for p in permissions:
            self.db.add(AdminPermission(role_id=role_id, permission_key=p, category=p.split(".")[0] if "." in p else "general"))
    async def remove_all_for_role(self, role_id: str):
        perms = await self.get_by_role(role_id)
        for p in perms: p.is_deleted = True
