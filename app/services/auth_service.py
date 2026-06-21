"""
Authentication service - Signup, login, 2FA, password reset, biometric logic.
"""

import hashlib
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
import pyotp
import qrcode
import io
import base64

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
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
from app.core.security import hash_password, verify_password
from app.core.config import settings
from app.utils.hashers import hash_user_password, check_user_password
from app.utils.generators import generate_otp, generate_uuid, generate_session_token
from app.utils.tokenizers import generate_access_token, generate_refresh_token_for_user, verify_token
from app.utils.encryptors import mask_and_encrypt_ssn
from app.core.email import send_email
from app.core.sms import send_sms
from app.services.account_service import AccountService


class AuthService:
    """Handles all authentication-related business logic."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)
    
    # ==================== SIGNUP ====================
    
    async def signup(self, data: Dict[str, Any], ip_address: Optional[str] = None) -> Tuple[bool, str, Optional[Dict]]:
        """Register a new user."""
        # Check if email exists
        if await self.repo.email_exists(data["email"]):
            return False, "Email already registered", None
        
        # Check if username exists
        if await self.repo.username_exists(data["username"]):
            return False, "Username already taken", None
        
        # Check if phone exists
        if await self.repo.phone_exists(data["phone"]):
            return False, "Phone number already registered", None
        
        # Create user
        user = User(
            email=data["email"].lower(),
            username=data["username"],
            phone=data["phone"],
            password_hash=hash_user_password(data["password"]),
        )
        user = await self.repo.create_user(user)
        
        # Create profile
        ssn_data = mask_and_encrypt_ssn(data["ssn"])
        profile = UserProfile(
            user_id=user.id,
            first_name=data["first_name"],
            last_name=data["last_name"],
            date_of_birth=datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date(),
            ssn_encrypted=ssn_data["encrypted"],
            ssn_last_four=ssn_data["masked"][-4:],
            address_line1=data["address_line1"],
            address_line2=data.get("address_line2"),
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
        )
        await self.repo.create_profile(profile)
        
        # Create security questions
        for i, (q, a) in enumerate([
            (data["security_question_1"], data["security_answer_1"]),
            (data["security_question_2"], data["security_answer_2"]),
        ], 1):
            sq = UserSecurityQuestion(
                user_id=user.id,
                question_number=i,
                question=q,
                answer_hash=hash_user_password(a.lower().strip()),
            )
            await self.repo.create_security_question(sq)
        
        # Create notification preferences
        prefs = UserNotificationPreference(user_id=user.id)
        await self.repo.create_notification_preferences(prefs)
        
        # AUTO-CREATE CHECKING ACCOUNT
        account_service = AccountService(self.db)
        await account_service.create_checking_account(user.id)
        
        # Send verification code
        code = generate_otp(6)
        expires = datetime.utcnow() + timedelta(minutes=30)
        await self.repo.set_verification_code(user.id, code, "email", expires)
        
        await send_email(
            to_email=user.email,
            subject="Verify your email - BankApp",
            body=f"Welcome to BankApp! Your verification code is: {code}",
            html_body=f"<h1>Welcome to BankApp!</h1><p>Your verification code is: <strong>{code}</strong></p><p>This code expires in 30 minutes.</p>",
        )
        
        await self.repo.log_activity(UserActivityLog(
            user_id=user.id,
            action="account_created",
            description="User account created with checking account",
            ip_address=ip_address,
        ))
        
        return True, "Account created. Please verify your email.", {
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
        }
    
    # ==================== LOGIN ====================
    
    async def login(
        self,
        login: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_name: Optional[str] = None,
        device_type: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[Dict]]:
        """Authenticate a user and create a session."""
        user = await self.repo.find_by_email_or_username(login)
        if not user:
            return False, "Invalid credentials", None
        
        if user.locked_until and user.locked_until > datetime.utcnow():
            remaining = int((user.locked_until - datetime.utcnow()).total_seconds() / 60)
            return False, f"Account is locked. Try again in {remaining} minutes", None
        
        if user.is_suspended:
            return False, "Account is suspended. Contact support.", None
        
        if not check_user_password(password, user.password_hash):
            await self.repo.increment_failed_attempts(user.id)
            await self.repo.log_login_attempt(UserLoginHistory(
                user_id=user.id, login_method="password", ip_address=ip_address,
                user_agent=user_agent, is_successful=False, failure_reason="Invalid password",
            ))
            return False, "Invalid credentials", None
        
        if not user.is_email_verified:
            return False, "Please verify your email before logging in", None
        
        await self.repo.reset_failed_attempts(user.id)
        
        if user.is_2fa_enabled:
            return True, "2FA required", {
                "requires_2fa": True,
                "user_id": user.id,
                "temp_token": generate_access_token(
                    {"sub": user.id, "purpose": "2fa_pending"},
                    expires_delta=timedelta(minutes=5),
                ),
            }
        
        return await self._create_login_session(user, ip_address, user_agent, device_name, device_type)
    
    async def _create_login_session(self, user, ip_address, user_agent, device_name, device_type):
        """Create a login session and return tokens."""
        session_id = generate_uuid()
        access_token = generate_access_token(user.id, user.email)
        refresh_token = generate_refresh_token_for_user(user.id, user.email)
        
        session = UserSession(
            id=session_id, user_id=user.id, access_token=access_token,
            refresh_token=refresh_token, ip_address=ip_address, user_agent=user_agent,
            device_name=device_name, device_type=device_type,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        await self.repo.create_session(session)
        
        await self.repo.log_login_attempt(UserLoginHistory(
            user_id=user.id, login_method="password", ip_address=ip_address,
            user_agent=user_agent, is_successful=True,
        ))
        
        await self.repo.log_activity(UserActivityLog(
            user_id=user.id, action="login", description="User logged in",
            ip_address=ip_address, user_agent=user_agent,
        ))
        
        profile = await self.repo.get_profile(user.id)
        
        return True, "Login successful", {
            "access_token": access_token, "refresh_token": refresh_token,
            "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "session_id": session_id, "requires_2fa": False,
            "user": {
                "id": user.id, "email": user.email, "username": user.username,
                "first_name": profile.first_name if profile else "",
                "last_name": profile.last_name if profile else "",
                "is_email_verified": user.is_email_verified,
                "is_phone_verified": user.is_phone_verified,
                "kyc_status": user.kyc_status,
            },
        }
    
    async def verify_email(self, user_id: str, code: str) -> Tuple[bool, str]:
        user = await self.repo.find_by_id(user_id)
        if not user: return False, "User not found"
        if user.is_email_verified: return False, "Email already verified"
        if user.email_verification_code != code: return False, "Invalid verification code"
        if user.email_verification_expires and user.email_verification_expires < datetime.utcnow():
            return False, "Verification code expired"
        await self.repo.update_email_verification(user.id)
        return True, "Email verified successfully"
    
    async def verify_phone(self, user_id: str, code: str) -> Tuple[bool, str]:
        user = await self.repo.find_by_id(user_id)
        if not user: return False, "User not found"
        if user.is_phone_verified: return False, "Phone already verified"
        if user.phone_verification_code != code: return False, "Invalid verification code"
        if user.phone_verification_expires and user.phone_verification_expires < datetime.utcnow():
            return False, "Verification code expired"
        await self.repo.update_phone_verification(user.id)
        return True, "Phone verified successfully"
    
    async def resend_verification(self, user_id: str, method: str) -> Tuple[bool, str]:
        user = await self.repo.find_by_id(user_id)
        if not user: return False, "User not found"
        code = generate_otp(6)
        expires = datetime.utcnow() + timedelta(minutes=30)
        if method == "email":
            if user.is_email_verified: return False, "Email already verified"
            await self.repo.set_verification_code(user.id, code, "email", expires)
            await send_email(to_email=user.email, subject="Verify your email - BankApp", body=f"Your code is: {code}")
        elif method == "phone":
            if user.is_phone_verified: return False, "Phone already verified"
            await self.repo.set_verification_code(user.id, code, "phone", expires)
            if user.phone: await send_sms(user.phone, f"Your code is: {code}")
        return True, f"New code sent to your {method}"
    
    async def forgot_password(self, email: str) -> Tuple[bool, str]:
        user = await self.repo.find_by_email(email)
        if not user: return True, "If an account exists, a reset link has been sent"
        token = generate_session_token()
        expires = datetime.utcnow() + timedelta(hours=1)
        await self.repo.set_password_reset_token(user.id, token, expires)
        await send_email(to_email=user.email, subject="Reset your password", body=f"Reset link: http://localhost:3000/reset-password?token={token}")
        return True, "If an account exists, a reset link has been sent"
    
    async def reset_password(self, token: str, new_password: str) -> Tuple[bool, str]:
        from sqlalchemy import select
        result = await self.db.execute(select(User).where(User.password_reset_token == token, User.password_reset_expires > datetime.utcnow(), User.is_deleted == False))
        user = result.scalar_one_or_none()
        if not user: return False, "Invalid or expired reset token"
        await self.repo.update_password(user.id, hash_user_password(new_password))
        await self.repo.clear_password_reset_token(user.id)
        await self.repo.deactivate_all_user_sessions(user.id)
        return True, "Password reset successful"
    
    async def forgot_username(self, email: str) -> Tuple[bool, str]:
        user = await self.repo.find_by_email(email)
        if not user: return True, "If an account exists, you will receive your username"
        await send_email(to_email=user.email, subject="Your username", body=f"Your username is: {user.username}")
        return True, "If an account exists, you will receive your username"
    
    async def refresh_token(self, refresh_token: str) -> Tuple[bool, str, Optional[Dict]]:
        payload = verify_token(refresh_token)
        if not payload: return False, "Invalid refresh token", None
        session = await self.repo.find_session_by_refresh_token(refresh_token)
        if not session: return False, "Session not found", None
        user = await self.repo.find_by_id(session.user_id)
        if not user or not user.is_active: return False, "Account not active", None
        new_access = generate_access_token(user.id, user.email)
        new_refresh = generate_refresh_token_for_user(user.id, user.email)
        session.access_token = new_access
        session.refresh_token = new_refresh
        session.expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        return True, "Token refreshed", {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer", "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60}
    
    async def logout(self, session_id: str) -> Tuple[bool, str]:
        await self.repo.deactivate_session(session_id)
        return True, "Logged out"
    
    async def setup_2fa(self, user_id: str, method: str = "authenticator", phone_number: Optional[str] = None) -> Tuple[bool, str, Optional[Dict]]:
        user = await self.repo.find_by_id(user_id)
        if not user: return False, "User not found", None
        if user.is_2fa_enabled: return False, "2FA already enabled", None
        secret = pyotp.random_base32()
        await self.repo.update_2fa_secret(user.id, secret)
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=user.email, issuer_name=settings.APP_NAME)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO(); img.save(buf, format="PNG")
        qr64 = base64.b64encode(buf.getvalue()).decode()
        return True, "2FA setup initiated", {"secret": secret, "qr_code_url": f"data:image/png;base64,{qr64}", "manual_key": secret}
    
    async def verify_2fa_setup(self, user_id: str, code: str) -> Tuple[bool, str]:
        user = await self.repo.find_by_id(user_id)
        if not user or not user.two_fa_secret: return False, "2FA not set up"
        totp = pyotp.TOTP(user.two_fa_secret)
        if totp.verify(code):
            await self.repo.enable_2fa(user.id)
            two_fa = User2FA(user_id=user.id, method_type="authenticator", secret=user.two_fa_secret, is_default=True, enabled_at=datetime.utcnow())
            await self.repo.create_2fa_method(two_fa)
            return True, "2FA enabled"
        return False, "Invalid code"
    
    async def verify_2fa_login(self, user_id, code, trust_device=False, device_name=None, device_type=None, ip_address=None, user_agent=None):
        user = await self.repo.find_by_id(user_id)
        if not user or not user.two_fa_secret: return False, "2FA not configured", None
        totp = pyotp.TOTP(user.two_fa_secret)
        if not totp.verify(code): return False, "Invalid 2FA code", None
        success, msg, data = await self._create_login_session(user, ip_address, user_agent, device_name, device_type)
        if success and trust_device and device_name:
            device = UserDevice(user_id=user.id, device_name=device_name, device_type=device_type, user_agent=user_agent, ip_address=ip_address, trusted_at=datetime.utcnow(), last_used_at=datetime.utcnow())
            await self.repo.create_device(device)
            data["trusted_device_id"] = device.id
        return success, msg, data
    
    async def disable_2fa(self, user_id, code, password):
        user = await self.repo.find_by_id(user_id)
        if not user: return False, "User not found"
        if not check_user_password(password, user.password_hash): return False, "Invalid password"
        if user.two_fa_secret:
            totp = pyotp.TOTP(user.two_fa_secret)
            if not totp.verify(code): return False, "Invalid 2FA code"
        await self.repo.disable_2fa(user.id)
        return True, "2FA disabled"
    
    async def setup_biometric(self, user_id, biometric_token, device_name, device_type=None):
        user = await self.repo.find_by_id(user_id)
        if not user: return False, "User not found"
        device_info = f"{device_name} ({device_type})" if device_type else device_name
        await self.repo.set_biometric_token(user.id, biometric_token, device_info)
        return True, "Biometric enabled"
    
    async def biometric_login(self, biometric_token, ip_address=None, user_agent=None):
        from sqlalchemy import select
        result = await self.db.execute(select(User).where(User.biometric_token == biometric_token, User.biometric_enabled == True, User.is_active == True, User.is_suspended == False, User.is_deleted == False))
        user = result.scalar_one_or_none()
        if not user: return False, "Invalid biometric", None
        return await self._create_login_session(user, ip_address, user_agent, "Biometric Device", "mobile")
    
    async def disable_biometric(self, user_id):
        await self.repo.disable_biometric(user_id)
        return True, "Biometric disabled"
