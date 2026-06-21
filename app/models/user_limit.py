"""
UserLimit model - Custom limits set per user by admin.
"""

from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserLimit(BaseModel, Base):
    """Custom limits overridden per user."""
    
    __tablename__ = "user_limits"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    daily_deposit_limit = Column(Float, nullable=True)
    daily_withdrawal_limit = Column(Float, nullable=True)
    daily_transfer_limit = Column(Float, nullable=True)
    per_transaction_limit = Column(Float, nullable=True)
    monthly_deposit_limit = Column(Float, nullable=True)
    monthly_withdrawal_limit = Column(Float, nullable=True)
    card_spending_limit = Column(Float, nullable=True)
    atm_withdrawal_limit = Column(Float, nullable=True)
    
    override_reason = Column(String(500), nullable=True)
    overridden_by = Column(String(36), nullable=True)
    
    def __repr__(self):
        return f"<UserLimit for {self.user_id}>"
