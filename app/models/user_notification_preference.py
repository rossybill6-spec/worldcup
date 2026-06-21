"""
UserNotificationPreference model - User's notification settings.
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserNotificationPreference(BaseModel, Base):
    """Notification preferences per user."""
    
    __tablename__ = "user_notification_preferences"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Push notifications
    push_enabled = Column(Boolean, default=True, nullable=False)
    push_deposits = Column(Boolean, default=True, nullable=False)
    push_withdrawals = Column(Boolean, default=True, nullable=False)
    push_transfers = Column(Boolean, default=True, nullable=False)
    push_security = Column(Boolean, default=True, nullable=False)
    push_promotions = Column(Boolean, default=False, nullable=False)
    
    # Email notifications
    email_enabled = Column(Boolean, default=True, nullable=False)
    email_deposits = Column(Boolean, default=True, nullable=False)
    email_withdrawals = Column(Boolean, default=True, nullable=False)
    email_transfers = Column(Boolean, default=True, nullable=False)
    email_security = Column(Boolean, default=True, nullable=False)
    email_promotions = Column(Boolean, default=False, nullable=False)
    email_statements = Column(Boolean, default=True, nullable=False)
    
    # SMS notifications
    sms_enabled = Column(Boolean, default=False, nullable=False)
    sms_deposits = Column(Boolean, default=False, nullable=False)
    sms_withdrawals = Column(Boolean, default=False, nullable=False)
    sms_security = Column(Boolean, default=True, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="notification_preferences")
    
    def __repr__(self):
        return f"<UserNotificationPreference for {self.user_id}>"
