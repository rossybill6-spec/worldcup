from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog

class AuditRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create(self, log: AuditLog): self.db.add(log)
    async def get_all(self, admin_id: str = None, action: str = None, page: int = 1, per_page: int = 50) -> tuple:
        q = select(AuditLog).order_by(AuditLog.created_at.desc())
        if admin_id: q = q.where(AuditLog.admin_id == admin_id)
        if action: q = q.where(AuditLog.action == action)
        total = (await self.db.execute(select(func.count()).select_from(q.subquery()))).scalar()
        rows = (await self.db.execute(q.offset((page-1)*per_page).limit(per_page))).scalars().all()
        return list(rows), total
