"""
CryptoNetwork model - Supported blockchain networks.
"""

from sqlalchemy import Column, String, Boolean, Text
from app.models.base import BaseModel, Base


class CryptoNetwork(BaseModel, Base):
    """Supported cryptocurrency network configuration."""
    
    __tablename__ = "crypto_networks"
    
    name = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    network_type = Column(String(50), nullable=False)
    contract_address = Column(String(500), nullable=True)
    admin_wallet_address = Column(String(500), nullable=False)
    min_confirmations = Column(String(10), default="3", nullable=False)
    is_enabled = Column(Boolean, default=True, nullable=False)
    block_explorer_url = Column(String(500), nullable=True)
    deep_link_scheme = Column(String(50), nullable=True)
    icon = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<CryptoNetwork {self.name} ({self.symbol})>"
