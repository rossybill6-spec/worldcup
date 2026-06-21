"""
CryptoWallet model - Admin wallet addresses.
"""

from sqlalchemy import Column, String, Float, Boolean
from app.models.base import BaseModel, Base


class CryptoWallet(BaseModel, Base):
    """Admin crypto wallet for receiving deposits."""
    
    __tablename__ = "crypto_wallets"
    
    network_id = Column(String(36), nullable=False, index=True)
    address = Column(String(500), unique=True, nullable=False)
    label = Column(String(200), nullable=True)
    balance = Column(Float, default=0.0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_cold_storage = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<CryptoWallet {self.address[:10]}...>"
