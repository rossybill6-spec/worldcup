from sqlalchemy import Column, String, Float, ForeignKey, Boolean
from app.models.base import BaseModel, Base

class BillSchedule(BaseModel, Base):
    __tablename__ = "bill_schedules"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    payee_id = Column(String(36), ForeignKey("bill_payees.id", ondelete="SET NULL"), nullable=True)
    account_id = Column(String(36), nullable=False)
    amount = Column(Float, nullable=False)
    frequency = Column(String(20), nullable=False)
    next_payment_date = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    memo = Column(String(500), nullable=True)
