"""
AccountBalance model - Daily balance snapshots.
"""

from sqlalchemy import Column, String, ForeignKey, Float, Date

from app.models.base import BaseModel, Base


class AccountBalance(BaseModel, Base):
    """Daily balance snapshot for an account."""
    
    __tablename__ = "account_balances"
    
    account_id = Column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    balance_date = Column(Date, nullable=False)
    opening_balance = Column(Float, default=0.0, nullable=False)
    closing_balance = Column(Float, default=0.0, nullable=False)
    total_credits = Column(Float, default=0.0, nullable=False)
    total_debits = Column(Float, default=0.0, nullable=False)
    transaction_count = Column(String(20), default="0", nullable=True)
    
    def __repr__(self):
        return f"<AccountBalance {self.balance_date} - {self.closing_balance}>"
