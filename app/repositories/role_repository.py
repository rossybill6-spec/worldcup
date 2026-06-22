from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.admin_role import AdminRole

class RoleRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def get_all(self) -> List[AdminRole]:
        r = await self.db.execute(select(AdminRole).where(AdminRole.is_deleted == False))
        return list(r.scalars().all())
    async def find_by_id(self, id: str) -> Optional[AdminRole]:
        r = await self.db.execute(select(AdminRole).where(AdminRole.id == id))
        return r.scalar_one_or_none()
    async def create(self, role: AdminRole) -> AdminRole: self.db.add(role); await self.db.flush(); return role
