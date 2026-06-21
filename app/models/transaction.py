from sqlalchemy import Column, String, Float, ForeignKey, Text
from app.models.base import BaseModel, Base

class Transaction(BaseModel, Base):
    __tablename__ = "transactions"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id = Column(String(36), nullable=True)
    transaction_type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    status = Column(String(20), default="completed")
    reference = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    source = Column(String(50), nullable=True)
    source_reference = Column(String(100), nullable=True)
    recipient = Column(String(200), nullable=True)
    category = Column(String(50), nullable=True)
    running_balance = Column(Float, nullable=True)
