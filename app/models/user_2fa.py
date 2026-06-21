"""
User2FA model - Two-factor authentication methods.
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class User2FA(BaseModel, Base):
    """2FA methods configured by the user."""
    
    __tablename__ = "user_2fa"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Method details
    method_type = Column(String(50), nullable=False)  # sms, authenticator, email
    is_enabled = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # For authenticator apps
    secret = Column(String(255), nullable=True)
    
    # For SMS
    phone_number = Column(String(20), nullable=True)
    
    # Timestamps
    enabled_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="two_fa_methods")
    
    def __repr__(self):
        return f"<User2FA {self.method_type} for {self.user_id}>"
