"""TransferTemplate model - Saved transfer templates for recurring transfers."""
from sqlalchemy import Column, String, Float, ForeignKey, Text, Boolean
from app.models.base import BaseModel, Base

class TransferTemplate(BaseModel, Base):
    __tablename__ = "transfer_templates"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    transfer_type = Column(String(50), nullable=False)
    from_account_id = Column(String(36), nullable=False)
    to_account_id = Column(String(36), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    recipient_name = Column(String(200), nullable=True)
    recipient_account = Column(String(50), nullable=True)
    recipient_routing = Column(String(20), nullable=True)
    recipient_bank = Column(String(200), nullable=True)
    swift_code = Column(String(20), nullable=True)
    memo = Column(Text, nullable=True)
    frequency = Column(String(20), nullable=True)
    next_run_date = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
