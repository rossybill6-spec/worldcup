"""
UserLoginHistory model - Records every login attempt.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserLoginHistory(BaseModel, Base):
    """Login attempt history for security auditing."""
    
    __tablename__ = "user_login_history"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Login details
    login_method = Column(String(50), nullable=False)  # password, biometric, 2fa
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_info = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    
    # Result
    is_successful = Column(Boolean, default=False, nullable=False)
    failure_reason = Column(String(200), nullable=True)
    
    # Timestamps
    attempted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="login_history")
    
    def __repr__(self):
        return f"<UserLoginHistory {self.user_id} - {'success' if self.is_successful else 'failed'}>"
