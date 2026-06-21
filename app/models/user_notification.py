"""
UserNotification model - In-app notifications for users.
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserNotification(BaseModel, Base):
    """In-app notifications."""
    
    __tablename__ = "user_notifications"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Notification content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(String(50), nullable=True)
    
    # Optional link/reference
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(String(36), nullable=True)
    extra_data = Column(JSON, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<UserNotification {self.notification_type} for {self.user_id}>"
