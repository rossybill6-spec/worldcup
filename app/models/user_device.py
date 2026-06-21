"""
UserDevice model - Trusted devices that can skip 2FA.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserDevice(BaseModel, Base):
    """Trusted devices for 2FA bypass."""
    
    __tablename__ = "user_devices"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Device info
    device_name = Column(String(200), nullable=False)
    device_type = Column(String(50), nullable=True)
    device_fingerprint = Column(String(500), nullable=True)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    # Trust status
    is_trusted = Column(Boolean, default=True, nullable=False)
    trusted_at = Column(DateTime, nullable=True)
    untrusted_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="devices")
    
    def __repr__(self):
        return f"<UserDevice {self.device_name}>"
