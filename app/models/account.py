"""
Account model - Checking and savings accounts.
"""

from sqlalchemy import Column, String, ForeignKey, Float, Boolean

from app.models.base import BaseModel, Base


class Account(BaseModel, Base):
    """Bank account (checking or savings)."""
    
    __tablename__ = "accounts"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    account_number = Column(String(20), unique=True, nullable=False, index=True)
    account_type = Column(String(20), nullable=False, default="checking")
    account_name = Column(String(100), nullable=True)
    balance = Column(Float, default=0.0, nullable=False)
    available_balance = Column(Float, default=0.0, nullable=False)
    pending_balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_frozen = Column(Boolean, default=False, nullable=False)
    interest_rate = Column(Float, default=0.0, nullable=False)
    overdraft_protection = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<Account {self.account_number} ({self.account_type})>"
