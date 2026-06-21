"""
CryptoTransaction model - Blockchain transaction records.
"""

from sqlalchemy import Column, String, Float
from app.models.base import BaseModel, Base


class CryptoTransaction(BaseModel, Base):
    """Recorded blockchain transaction."""
    
    __tablename__ = "crypto_transactions"
    
    tx_hash = Column(String(500), unique=True, nullable=False, index=True)
    network = Column(String(50), nullable=False)
    from_address = Column(String(500), nullable=True)
    to_address = Column(String(500), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    confirmations = Column(String(10), default="0", nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    deposit_session_id = Column(String(36), nullable=True, index=True)
    user_id = Column(String(36), nullable=True)
    
    def __repr__(self):
        return f"<CryptoTransaction {self.tx_hash[:10]}...>"
