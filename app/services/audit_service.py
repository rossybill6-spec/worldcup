from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.audit_repository import AuditRepository

class AuditService:
    def __init__(self, db: AsyncSession): self.db = db; self.repo = AuditRepository(db)
    async def get_logs(self, admin_id: str = None, action: str = None, page: int = 1, per_page: int = 50) -> Dict:
        logs, total = await self.repo.get_all(admin_id, action, page, per_page)
        items = [{"id": l.id, "admin_name": l.admin_name, "action": l.action, "target_type": l.target_type, "target_id": l.target_id, "details": l.details, "ip_address": l.ip_address, "before_value": l.before_value, "after_value": l.after_value, "created_at": l.created_at.isoformat() if l.created_at else None} for l in logs]
        return {"items": items, "total": total, "page": page, "per_page": per_page}
