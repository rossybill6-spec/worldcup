from typing import Dict
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.admin_repository import AdminRepository
from app.models.admin import Admin
from app.models.admin_session import AdminSession
from app.models.admin_activity_log import AdminActivityLog
from app.utils.hashers import check_user_password
from app.core.security import create_access_token
from app.utils.generators import generate_uuid
from app.core.config import settings

class AdminService:
    def __init__(self, db: AsyncSession): self.db = db; self.repo = AdminRepository(db)
    
    async def login(self, email: str, password: str, ip: str = None, ua: str = None) -> Dict:
        admin = await self.repo.find_by_email(email)
        if not admin or not admin.is_active: return {"success": False, "message": "Invalid credentials"}
        if not check_user_password(password, admin.password_hash): return {"success": False, "message": "Invalid credentials"}
        payload = {"sub": admin.id, "email": admin.email, "role": "admin", "is_admin": True}
        access = create_access_token(payload, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh = create_access_token({"sub": admin.id, "type": "admin_refresh"}, timedelta(days=7))
        session = AdminSession(admin_id=admin.id, access_token=access, refresh_token=refresh, ip_address=ip, user_agent=ua, expires_at=datetime.utcnow() + timedelta(days=7))
        await self.repo.create_session(session)
        admin.last_login_at = datetime.utcnow()
        await self.repo.log_activity(AdminActivityLog(admin_id=admin.id, admin_name=admin.full_name, action="login", ip_address=ip))
        return {"success": True, "access_token": access, "refresh_token": refresh, "token_type": "bearer", "admin_id": admin.id, "full_name": admin.full_name, "email": admin.email, "is_super_admin": admin.is_super_admin, "permissions": []}
    
    async def get_dashboard_stats(self) -> Dict:
        return {"total_users": await self.repo.count_users(), "pending_deposits": await self.repo.count_pending_deposits(), "pending_withdrawals": await self.repo.count_pending_withdrawals(), "total_balance": await self.repo.total_balance()}
