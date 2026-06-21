"""
User repository - All database operations for users.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_session import UserSession
from app.models.user_device import UserDevice
from app.models.user_login_history import UserLoginHistory
from app.models.user_activity_log import UserActivityLog
from app.models.user_security_question import UserSecurityQuestion
from app.models.user_2fa import User2FA
from app.models.user_notification import UserNotification
from app.models.user_notification_preference import UserNotificationPreference


class UserRepository:
    """Repository for all user-related database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ========== FIND BY ==========
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id, User.is_deleted == False))
        return result.scalar_one_or_none()
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        result = await self.db.execute(
            select(User).where(User.email == email.lower(), User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def find_by_email_or_username(self, login: str) -> Optional[User]:
        """Find user by email or username."""
        result = await self.db.execute(
            select(User).where(
                (User.email == login.lower()) | (User.username == login),
                User.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()
    
    async def find_by_phone(self, phone: str) -> Optional[User]:
        """Find user by phone number."""
        result = await self.db.execute(
            select(User).where(User.phone == phone, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    # ========== CREATE ==========
    
    async def create_user(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        await self.db.flush()
        return user
    
    async def create_profile(self, profile: UserProfile) -> UserProfile:
        """Create user profile."""
        self.db.add(profile)
        await self.db.flush()
        return profile
    
    # ========== UPDATE ==========
    
    async def update_password(self, user_id: str, password_hash: str) -> None:
        """Update user password."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                password_hash=password_hash,
                password_changed_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
    
    async def update_email_verification(self, user_id: str) -> None:
        """Mark email as verified."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                is_email_verified=True,
                email_verification_code=None,
                email_verification_expires=None,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def update_phone_verification(self, user_id: str) -> None:
        """Mark phone as verified."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                is_phone_verified=True,
                phone_verification_code=None,
                phone_verification_expires=None,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def set_verification_code(self, user_id: str, code: str, field: str, expires: datetime) -> None:
        """Set email or phone verification code."""
        values = {"updated_at": datetime.utcnow()}
        if field == "email":
            values["email_verification_code"] = code
            values["email_verification_expires"] = expires
        elif field == "phone":
            values["phone_verification_code"] = code
            values["phone_verification_expires"] = expires
        
        await self.db.execute(
            update(User).where(User.id == user_id).values(**values)
        )
    
    async def set_password_reset_token(self, user_id: str, token: str, expires: datetime) -> None:
        """Set password reset token."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                password_reset_token=token,
                password_reset_expires=expires,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def clear_password_reset_token(self, user_id: str) -> None:
        """Clear password reset token after use."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                password_reset_token=None,
                password_reset_expires=None,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def increment_failed_attempts(self, user_id: str) -> None:
        """Increment failed login attempts."""
        user = await self.find_by_id(user_id)
        if user:
            attempts = user.failed_login_attempts + 1
            values = {
                "failed_login_attempts": attempts,
                "updated_at": datetime.utcnow(),
            }
            if attempts >= 5:
                values["locked_until"] = datetime.utcnow().replace(hour=23, minute=59, second=59)
                # Lock for 30 minutes
                from datetime import timedelta
                values["locked_until"] = datetime.utcnow() + timedelta(minutes=30)
            
            await self.db.execute(
                update(User).where(User.id == user_id).values(**values)
            )
    
    async def reset_failed_attempts(self, user_id: str) -> None:
        """Reset failed login attempts on successful login."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                failed_login_attempts=0,
                locked_until=None,
                last_login_at=datetime.utcnow(),
                last_activity_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
    
    async def update_2fa_secret(self, user_id: str, secret: str) -> None:
        """Set 2FA secret."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                two_fa_secret=secret,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def enable_2fa(self, user_id: str) -> None:
        """Enable 2FA for user."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                is_2fa_enabled=True,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def disable_2fa(self, user_id: str) -> None:
        """Disable 2FA for user."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                is_2fa_enabled=False,
                two_fa_secret=None,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def set_biometric_token(self, user_id: str, token: str, device_info: str) -> None:
        """Set biometric login token."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                biometric_enabled=True,
                biometric_token=token,
                biometric_device_info=device_info,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def disable_biometric(self, user_id: str) -> None:
        """Disable biometric login."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                biometric_enabled=False,
                biometric_token=None,
                biometric_device_info=None,
                updated_at=datetime.utcnow(),
            )
        )
    
    async def update_last_activity(self, user_id: str) -> None:
        """Update last activity timestamp."""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_activity_at=datetime.utcnow())
        )
    
    # ========== SESSIONS ==========
    
    async def create_session(self, session: UserSession) -> UserSession:
        """Create a new user session."""
        self.db.add(session)
        await self.db.flush()
        return session
    
    async def find_session_by_id(self, session_id: str) -> Optional[UserSession]:
        """Find session by ID."""
        result = await self.db.execute(
            select(UserSession).where(UserSession.id == session_id, UserSession.is_active == True)
        )
        return result.scalar_one_or_none()
    
    async def find_session_by_refresh_token(self, refresh_token: str) -> Optional[UserSession]:
        """Find session by refresh token."""
        result = await self.db.execute(
            select(UserSession).where(
                UserSession.refresh_token == refresh_token,
                UserSession.is_active == True,
            )
        )
        return result.scalar_one_or_none()
    
    async def deactivate_session(self, session_id: str) -> None:
        """Deactivate a session (logout)."""
        await self.db.execute(
            update(UserSession)
            .where(UserSession.id == session_id)
            .values(
                is_active=False,
                logged_out_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
    
    async def deactivate_all_user_sessions(self, user_id: str, except_session_id: Optional[str] = None) -> None:
        """Deactivate all sessions for a user except one."""
        stmt = update(UserSession).where(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
        )
        if except_session_id:
            stmt = stmt.where(UserSession.id != except_session_id)
        
        await self.db.execute(
            stmt.values(
                is_active=False,
                logged_out_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
    
    async def get_user_sessions(self, user_id: str) -> List[UserSession]:
        """Get all active sessions for a user."""
        result = await self.db.execute(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.is_active == True,
            )
        )
        return list(result.scalars().all())
    
    # ========== DEVICES ==========
    
    async def create_device(self, device: UserDevice) -> UserDevice:
        """Register a trusted device."""
        self.db.add(device)
        await self.db.flush()
        return device
    
    async def get_user_devices(self, user_id: str) -> List[UserDevice]:
        """Get all trusted devices for a user."""
        result = await self.db.execute(
            select(UserDevice).where(
                UserDevice.user_id == user_id,
                UserDevice.is_trusted == True,
                UserDevice.is_deleted == False,
            )
        )
        return list(result.scalars().all())
    
    async def untrust_device(self, device_id: str) -> None:
        """Remove trust from a device."""
        await self.db.execute(
            update(UserDevice)
            .where(UserDevice.id == device_id)
            .values(
                is_trusted=False,
                untrusted_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
    
    async def find_device_by_id(self, device_id: str) -> Optional[UserDevice]:
        """Find a device by ID."""
        result = await self.db.execute(select(UserDevice).where(UserDevice.id == device_id))
        return result.scalar_one_or_none()
    
    # ========== LOGIN HISTORY ==========
    
    async def log_login_attempt(self, history: UserLoginHistory) -> None:
        """Record a login attempt."""
        self.db.add(history)
        await self.db.flush()
    
    async def get_login_history(self, user_id: str, limit: int = 20) -> List[UserLoginHistory]:
        """Get login history for a user."""
        result = await self.db.execute(
            select(UserLoginHistory)
            .where(UserLoginHistory.user_id == user_id)
            .order_by(UserLoginHistory.attempted_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    # ========== ACTIVITY LOG ==========
    
    async def log_activity(self, activity: UserActivityLog) -> None:
        """Record user activity."""
        self.db.add(activity)
        await self.db.flush()
    
    async def get_activity_logs(self, user_id: str, limit: int = 50, offset: int = 0) -> List[UserActivityLog]:
        """Get activity logs for a user."""
        result = await self.db.execute(
            select(UserActivityLog)
            .where(UserActivityLog.user_id == user_id)
            .order_by(UserActivityLog.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    # ========== SECURITY QUESTIONS ==========
    
    async def create_security_question(self, question: UserSecurityQuestion) -> None:
        """Save a security question."""
        self.db.add(question)
        await self.db.flush()
    
    async def get_security_questions(self, user_id: str) -> List[UserSecurityQuestion]:
        """Get security questions for a user."""
        result = await self.db.execute(
            select(UserSecurityQuestion).where(UserSecurityQuestion.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def verify_security_answer(self, user_id: str, question_number: int, answer_hash: str) -> bool:
        """Verify a security question answer."""
        result = await self.db.execute(
            select(UserSecurityQuestion).where(
                UserSecurityQuestion.user_id == user_id,
                UserSecurityQuestion.question_number == question_number,
                UserSecurityQuestion.answer_hash == answer_hash,
            )
        )
        return result.scalar_one_or_none() is not None
    
    # ========== 2FA METHODS ==========
    
    async def create_2fa_method(self, two_fa: User2FA) -> None:
        """Add a 2FA method."""
        self.db.add(two_fa)
        await self.db.flush()
    
    async def get_2fa_methods(self, user_id: str) -> List[User2FA]:
        """Get 2FA methods for a user."""
        result = await self.db.execute(
            select(User2FA).where(User2FA.user_id == user_id, User2FA.is_enabled == True)
        )
        return list(result.scalars().all())
    
    # ========== NOTIFICATIONS ==========
    
    async def create_notification(self, notification: UserNotification) -> None:
        """Create an in-app notification."""
        self.db.add(notification)
        await self.db.flush()
    
    async def create_notification_preferences(self, prefs: UserNotificationPreference) -> None:
        """Create default notification preferences."""
        self.db.add(prefs)
        await self.db.flush()
    
    # ========== PROFILE ==========
    
    async def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile."""
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_profile(self, user_id: str, **kwargs) -> None:
        """Update user profile fields."""
        kwargs["updated_at"] = datetime.utcnow()
        await self.db.execute(
            update(UserProfile)
            .where(UserProfile.user_id == user_id)
            .values(**kwargs)
        )
    
    # ========== COUNT & EXISTS ==========
    
    async def email_exists(self, email: str) -> bool:
        """Check if email already registered."""
        result = await self.db.execute(
            select(func.count(User.id)).where(User.email == email.lower(), User.is_deleted == False)
        )
        return result.scalar() > 0
    
    async def username_exists(self, username: str) -> bool:
        """Check if username already taken."""
        result = await self.db.execute(
            select(func.count(User.id)).where(User.username == username, User.is_deleted == False)
        )
        return result.scalar() > 0
    
    async def phone_exists(self, phone: str) -> bool:
        """Check if phone already registered."""
        result = await self.db.execute(
            select(func.count(User.id)).where(User.phone == phone, User.is_deleted == False)
        )
        return result.scalar() > 0
