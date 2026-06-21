"""Transfer model - All transfer transactions."""
from sqlalchemy import Column, String, Float, ForeignKey, Text, Boolean
from app.models.base import BaseModel, Base

class Transfer(BaseModel, Base):
    __tablename__ = "transfers"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    from_account_id = Column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    to_account_id = Column(String(36), nullable=True)
    transfer_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0, nullable=False)
    net_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    exchange_rate = Column(Float, nullable=True)
    converted_amount = Column(Float, nullable=True)
    status = Column(String(20), default="pending", nullable=False)
    reference = Column(String(50), unique=True, nullable=False, index=True)
    recipient_name = Column(String(200), nullable=True)
    recipient_account = Column(String(50), nullable=True)
    recipient_routing = Column(String(20), nullable=True)
    recipient_bank = Column(String(200), nullable=True)
    swift_code = Column(String(20), nullable=True)
    memo = Column(Text, nullable=True)
    is_recurring = Column(Boolean, default=False, nullable=False)
    template_id = Column(String(36), nullable=True)
    admin_notes = Column(Text, nullable=True)
    approved_by = Column(String(36), nullable=True)
    approved_at = Column(String(50), nullable=True)
