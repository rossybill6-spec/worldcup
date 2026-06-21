from sqlalchemy import Column, String, ForeignKey, Text
from app.models.base import BaseModel, Base

class TransactionDispute(BaseModel, Base):
    __tablename__ = "transaction_disputes"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_id = Column(String(36), nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String(20), default="open")
    resolution = Column(Text, nullable=True)
    resolved_by = Column(String(36), nullable=True)
    resolved_at = Column(String(50), nullable=True)
