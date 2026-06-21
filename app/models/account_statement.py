"""
AccountStatement model - Monthly account statements.
"""

from sqlalchemy import Column, String, ForeignKey, Float, Date

from app.models.base import BaseModel, Base


class AccountStatement(BaseModel, Base):
    """Monthly account statement."""
    
    __tablename__ = "account_statements"
    
    account_id = Column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    statement_date = Column(Date, nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    opening_balance = Column(Float, default=0.0, nullable=False)
    closing_balance = Column(Float, default=0.0, nullable=False)
    total_deposits = Column(Float, default=0.0, nullable=False)
    total_withdrawals = Column(Float, default=0.0, nullable=False)
    total_fees = Column(Float, default=0.0, nullable=False)
    interest_earned = Column(Float, default=0.0, nullable=False)
    file_url = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<AccountStatement {self.statement_date}>"
