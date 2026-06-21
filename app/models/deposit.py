"""
Deposit model - All deposit transactions.
"""

from sqlalchemy import Column, String, Float, ForeignKey, Text
from app.models.base import BaseModel, Base


class Deposit(BaseModel, Base):
    """Deposit transaction record."""
    
    __tablename__ = "deposits"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id = Column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    
    method = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0, nullable=False)
    net_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    reference = Column(String(50), unique=True, nullable=False, index=True)
    
    # Method-specific data stored as comma-separated or JSON string
    method_data = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    approved_by = Column(String(36), nullable=True)
    approved_at = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<Deposit {self.reference} - {self.status}>"
