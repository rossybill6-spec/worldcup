"""
UserDocument model - KYC document uploads.
"""

from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserDocument(BaseModel, Base):
    """KYC documents uploaded by users."""
    
    __tablename__ = "user_documents"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    document_type = Column(String(50), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=True)
    file_size = Column(String(50), nullable=True)
    verification_status = Column(String(20), default="pending", nullable=False)
    verified_by = Column(String(36), nullable=True)
    verified_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<UserDocument {self.document_type} - {self.verification_status}>"
