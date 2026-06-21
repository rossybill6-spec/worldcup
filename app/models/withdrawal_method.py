"""
WithdrawalMethod model - Configurable withdrawal method definitions.
"""
from sqlalchemy import Column, String, Float, Boolean, Text
from app.models.base import BaseModel, Base

class WithdrawalMethod(BaseModel, Base):
    __tablename__ = "withdrawal_methods"
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=True, nullable=False)
    min_amount = Column(Float, default=0.01, nullable=False)
    max_amount = Column(Float, default=1000000.0, nullable=False)
    fee_type = Column(String(20), default="flat", nullable=False)
    fee_amount = Column(Float, default=0.0, nullable=False)
    processing_time = Column(String(100), nullable=True)
    requires_admin_approval = Column(Boolean, default=True, nullable=False)
    display_order = Column(String(20), default="99", nullable=True)
    icon = Column(String(50), nullable=True)
