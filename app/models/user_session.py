"""
UserSession model - Tracks active user login sessions.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserSession(BaseModel, Base):
    """Active user login sessions."""
    
    __tablename__ = "user_sessions"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Token info
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    
    # Device & Location
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_type = Column(String(50), nullable=True)
    device_name = Column(String(200), nullable=True)
    location = Column(String(200), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    logged_out_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession {self.id} for user {self.user_id}>"
