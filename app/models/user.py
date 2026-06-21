"""
User model - Core user account information.
"""

from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class User(BaseModel, Base):
    """Main user account table."""
    
    __tablename__ = "users"
    
    # Identity
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=True)
    
    # Security
    password_hash = Column(String(255), nullable=False)
    pin_hash = Column(String(255), nullable=True)
    
    # Verification
    is_email_verified = Column(Boolean, default=False, nullable=False)
    is_phone_verified = Column(Boolean, default=False, nullable=False)
    email_verification_code = Column(String(10), nullable=True)
    email_verification_expires = Column(DateTime, nullable=True)
    phone_verification_code = Column(String(10), nullable=True)
    phone_verification_expires = Column(DateTime, nullable=True)
    
    # Account Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_suspended = Column(Boolean, default=False, nullable=False)
    suspended_reason = Column(Text, nullable=True)
    suspended_at = Column(DateTime, nullable=True)
    
    # Lockout
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    
    # 2FA
    is_2fa_enabled = Column(Boolean, default=False, nullable=False)
    two_fa_secret = Column(String(255), nullable=True)
    
    # Biometric
    biometric_enabled = Column(Boolean, default=False, nullable=False)
    biometric_token = Column(String(500), nullable=True)
    biometric_device_info = Column(Text, nullable=True)
    
    # KYC
    kyc_status = Column(String(20), default="not_submitted", nullable=False)
    kyc_submitted_at = Column(DateTime, nullable=True)
    kyc_verified_at = Column(DateTime, nullable=True)
    kyc_rejection_reason = Column(Text, nullable=True)
    
    # Password Reset
    password_reset_token = Column(String(500), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    
    # Timestamps
    last_login_at = Column(DateTime, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, nullable=True)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    devices = relationship("UserDevice", back_populates="user", cascade="all, delete-orphan")
    login_history = relationship("UserLoginHistory", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("UserActivityLog", back_populates="user", cascade="all, delete-orphan")
    security_questions = relationship("UserSecurityQuestion", back_populates="user", cascade="all, delete-orphan")
    two_fa_methods = relationship("User2FA", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("UserNotification", back_populates="user", cascade="all, delete-orphan")
    notification_preferences = relationship("UserNotificationPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"
