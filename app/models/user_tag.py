"""
UserTag model - Tags/labels applied to users by admin.
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserTag(BaseModel, Base):
    """Tags applied to users (VIP, flagged, etc.)."""
    
    __tablename__ = "user_tags"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tag = Column(String(100), nullable=False)
    applied_by = Column(String(36), nullable=True)
    
    def __repr__(self):
        return f"<UserTag {self.tag}>"
