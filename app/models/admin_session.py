from sqlalchemy import Column, String, DateTime, Boolean, Text
from app.models.base import BaseModel, Base

class AdminSession(BaseModel, Base):
    __tablename__ = "admin_sessions"
    admin_id = Column(String(36), nullable=False, index=True)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=False)
    logged_out_at = Column(DateTime, nullable=True)
