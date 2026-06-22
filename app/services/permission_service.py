from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.permission_repository import PermissionRepository

class PermissionService:
    def __init__(self, db: AsyncSession): self.db = db; self.repo = PermissionRepository(db)
    async def get_permissions(self, role_id: str) -> List[str]:
        perms = await self.repo.get_by_role(role_id)
        return [p.permission_key for p in perms]
    async def assign_permissions(self, role_id: str, permissions: List[str]):
        await self.repo.remove_all_for_role(role_id)
        await self.repo.assign(role_id, permissions)
