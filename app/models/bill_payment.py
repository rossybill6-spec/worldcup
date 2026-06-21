from sqlalchemy import Column, String, Float, ForeignKey, Text, Boolean
from app.models.base import BaseModel, Base

class BillPayment(BaseModel, Base):
    __tablename__ = "bill_payments"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id = Column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    payee_id = Column(String(36), ForeignKey("bill_payees.id", ondelete="SET NULL"), nullable=True)
    amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0, nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    reference = Column(String(50), unique=True, nullable=False, index=True)
    scheduled_date = Column(String(50), nullable=True)
    is_recurring = Column(Boolean, default=False, nullable=False)
    frequency = Column(String(20), nullable=True)
    memo = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
