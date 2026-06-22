from sqlalchemy import Column, String, Text, Boolean
from app.models.base import BaseModel, Base
class LegalDocument(BaseModel, Base):
    __tablename__ = "legal_documents"
    name = Column(String(100), nullable=False)
    document_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    version = Column(String(20), nullable=False)
    is_current = Column(Boolean, default=False)
    published_at = Column(String(50), nullable=True)
