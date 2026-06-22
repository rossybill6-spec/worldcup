from sqlalchemy import Column, String, Boolean, DateTime, Text
from app.models.base import BaseModel, Base

class Admin(BaseModel, Base):
    __tablename__ = "admins"
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=False)
    role_id = Column(String(36), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    is_super_admin = Column(Boolean, default=False)
    failed_login_attempts = Column(String(10), default="0")
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    ip_whitelist = Column(Text, nullable=True)
    working_hours_start = Column(String(5), nullable=True)
    working_hours_end = Column(String(5), nullable=True)
    two_fa_secret = Column(String(255), nullable=True)
    is_2fa_enabled = Column(Boolean, default=False)
