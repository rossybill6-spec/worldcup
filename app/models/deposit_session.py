"""
DepositSession model - Active crypto deposit sessions.
"""

from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from app.models.base import BaseModel, Base


class DepositSession(BaseModel, Base):
    """Crypto deposit session with wallet address and expiry."""
    
    __tablename__ = "deposit_sessions"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    deposit_id = Column(String(36), ForeignKey("deposits.id", ondelete="CASCADE"), nullable=True)
    
    network = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=False)
    expected_amount = Column(Float, nullable=True)
    admin_address = Column(String(500), nullable=False)
    reference = Column(String(50), unique=True, nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    expires_at = Column(DateTime, nullable=False)
    tx_hash = Column(String(500), nullable=True)
    confirmed_at = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<DepositSession {self.reference} - {self.network}>"
