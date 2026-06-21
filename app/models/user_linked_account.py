"""
UserLinkedAccount model - External bank accounts linked by user.
"""

from sqlalchemy import Column, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserLinkedAccount(BaseModel, Base):
    """External bank accounts linked for ACH transfers."""
    
    __tablename__ = "user_linked_accounts"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    bank_name = Column(String(200), nullable=False)
    account_number = Column(String(50), nullable=False)
    routing_number = Column(String(20), nullable=False)
    account_type = Column(String(20), default="checking", nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_method = Column(String(20), nullable=True)
    micro_deposit_1 = Column(Float, nullable=True)
    micro_deposit_2 = Column(Float, nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    plaid_token = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<UserLinkedAccount {self.bank_name} - {'verified' if self.is_verified else 'unverified'}>"
