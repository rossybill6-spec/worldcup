"""
UserNote model - Internal admin notes about users.
"""

from sqlalchemy import Column, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserNote(BaseModel, Base):
    """Internal notes about users (admin only)."""
    
    __tablename__ = "user_notes"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    note = Column(Text, nullable=False)
    author_id = Column(String(36), nullable=True)
    author_name = Column(String(200), nullable=True)
    is_pinned = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<UserNote by {self.author_name}>"
