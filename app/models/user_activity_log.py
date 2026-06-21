"""
UserActivityLog model - Tracks user actions within the app.
"""

from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserActivityLog(BaseModel, Base):
    """User activity audit trail."""
    
    __tablename__ = "user_activity_logs"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Activity details
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    extra_data = Column(JSON, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="activity_logs")
    
    def __repr__(self):
        return f"<UserActivityLog {self.action} by {self.user_id}>"
