"""
User service - Profile management, security settings, sessions, devices.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_activity_log import UserActivityLog
from app.models.user_security_question import UserSecurityQuestion
from app.utils.hashers import hash_user_password, check_user_password, hash_user_pin, check_user_pin


class UserService:
    """Handles user profile and settings business logic."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)
    
    # ==================== PROFILE ====================
    
    async def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get full user profile with all details."""
        user = await self.repo.find_by_id(user_id)
        if not user:
            return None
        
        profile = await self.repo.get_profile(user_id)
        
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "phone": user.phone,
            "is_email_verified": user.is_email_verified,
            "is_phone_verified": user.is_phone_verified,
            "is_2fa_enabled": user.is_2fa_enabled,
            "biometric_enabled": user.biometric_enabled,
            "kyc_status": user.kyc_status,
            "is_active": user.is_active,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "first_name": profile.first_name if profile else None,
            "last_name": profile.last_name if profile else None,
            "date_of_birth": profile.date_of_birth.isoformat() if profile and profile.date_of_birth else None,
            "ssn_last_four": profile.ssn_last_four if profile else None,
            "address_line1": profile.address_line1 if profile else None,
            "address_line2": profile.address_line2 if profile else None,
            "city": profile.city if profile else None,
            "state": profile.state if profile else None,
            "zip_code": profile.zip_code if profile else None,
            "profile_picture_url": profile.profile_picture_url if profile else None,
        }
    
    async def update_profile(self, user_id: str, data: Dict[str, Any]) -> bool:
        """Update user profile fields."""
        allowed_fields = [
            "first_name", "last_name", "phone", "address_line1", "address_line2",
            "city", "state", "zip_code", "occupation", "employer",
        ]
        update_data = {k: v for k, v in data.items() if k in allowed_fields and v is not None}
        
        if not update_data:
            return False
        
        await self.repo.update_profile(user_id, **update_data)
        await self.repo.log_activity(UserActivityLog(
            user_id=user_id,
            action="profile_updated",
            description=f"Updated fields: {', '.join(update_data.keys())}",
        ))
        
        return True
    
    # ==================== SECURITY ====================
    
    async def change_password(self, user_id: str, current_password: str, new_password: str) -> tuple:
        """Change user password."""
        user = await self.repo.find_by_id(user_id)
        if not user:
            return False, "User not found"
        
        if not check_user_password(current_password, user.password_hash):
            return False, "Current password is incorrect"
        
        await self.repo.update_password(user_id, hash_user_password(new_password))
        await self.repo.deactivate_all_user_sessions(user_id)
        
        await self.repo.log_activity(UserActivityLog(
            user_id=user_id,
            action="password_changed",
            description="Password changed",
        ))
        
        return True, "Password changed successfully"
    
    async def change_pin(self, user_id: str, current_pin: str, new_pin: str) -> tuple:
        """Change user PIN."""
        user = await self.repo.find_by_id(user_id)
        if not user:
            return False, "User not found"
        
        if user.pin_hash and not check_user_pin(current_pin, user.pin_hash):
            return False, "Current PIN is incorrect"
        
        from sqlalchemy import update
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(pin_hash=hash_user_pin(new_pin), updated_at=datetime.utcnow())
        )
        
        await self.repo.log_activity(UserActivityLog(
            user_id=user_id,
            action="pin_changed",
            description="PIN changed",
        ))
        
        return True, "PIN changed successfully"
    
    # ==================== SESSIONS ====================
    
    async def get_sessions(self, user_id: str) -> List[Dict]:
        """Get all active sessions for a user."""
        sessions = await self.repo.get_user_sessions(user_id)
        return [
            {
                "id": s.id,
                "ip_address": s.ip_address,
                "device_name": s.device_name,
                "device_type": s.device_type,
                "location": s.location,
                "is_active": s.is_active,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "expires_at": s.expires_at.isoformat() if s.expires_at else None,
            }
            for s in sessions
        ]
    
    async def revoke_session(self, user_id: str, session_id: str) -> bool:
        """Revoke a specific session."""
        session = await self.repo.find_session_by_id(session_id)
        if not session or session.user_id != user_id:
            return False
        await self.repo.deactivate_session(session_id)
        return True
    
    # ==================== DEVICES ====================
    
    async def get_devices(self, user_id: str) -> List[Dict]:
        """Get all trusted devices."""
        devices = await self.repo.get_user_devices(user_id)
        return [
            {
                "id": d.id,
                "device_name": d.device_name,
                "device_type": d.device_type,
                "is_trusted": d.is_trusted,
                "last_used_at": d.last_used_at.isoformat() if d.last_used_at else None,
                "created_at": d.created_at.isoformat() if d.created_at else None,
            }
            for d in devices
        ]
    
    async def untrust_device(self, user_id: str, device_id: str) -> bool:
        """Remove trust from a device."""
        device = await self.repo.find_device_by_id(device_id)
        if not device or device.user_id != user_id:
            return False
        await self.repo.untrust_device(device_id)
        return True
    
    # ==================== LOGIN HISTORY ====================
    
    async def get_login_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get login history."""
        history = await self.repo.get_login_history(user_id, limit)
        return [
            {
                "id": h.id,
                "login_method": h.login_method,
                "ip_address": h.ip_address,
                "device_info": h.device_info,
                "location": h.location,
                "is_successful": h.is_successful,
                "failure_reason": h.failure_reason,
                "attempted_at": h.attempted_at.isoformat() if h.attempted_at else None,
            }
            for h in history
        ]
    
    # ==================== ACTIVITY LOG ====================
    
    async def get_activity_logs(self, user_id: str, page: int = 1, per_page: int = 50) -> tuple:
        """Get paginated activity logs."""
        offset = (page - 1) * per_page
        logs = await self.repo.get_activity_logs(user_id, per_page, offset)
        items = [
            {
                "id": log.id,
                "action": log.action,
                "description": log.description,
                "ip_address": log.ip_address,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ]
        return items, len(items)
    
    # ==================== SECURITY QUESTIONS ====================
    
    async def get_security_questions(self, user_id: str) -> List[Dict]:
        """Get user's security questions (masked answers)."""
        questions = await self.repo.get_security_questions(user_id)
        return [
            {
                "id": q.id,
                "question_number": q.question_number,
                "question": q.question,
            }
            for q in questions
        ]
    
    # ==================== CLOSE ACCOUNT ====================
    
    async def close_account(self, user_id: str, reason: str, destination: Optional[str] = None) -> tuple:
        """Close user account."""
        from sqlalchemy import update
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                is_active=False,
                is_deleted=True,
                deleted_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        await self.repo.deactivate_all_user_sessions(user_id)
        await self.repo.log_activity(UserActivityLog(
            user_id=user_id,
            action="account_closed",
            description=f"Account closed. Reason: {reason}",
        ))
        return True, "Account closed"
