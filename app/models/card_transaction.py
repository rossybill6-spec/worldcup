from sqlalchemy import Column, String, Float, ForeignKey
from app.models.base import BaseModel, Base

class CardTransaction(BaseModel, Base):
    __tablename__ = "card_transactions"
    card_id = Column(String(36), ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    merchant = Column(String(200), nullable=True)
    category = Column(String(50), nullable=True)
    status = Column(String(20), default="completed", nullable=False)
    transaction_type = Column(String(20), default="purchase", nullable=False)
    reference = Column(String(50), nullable=True)
    location = Column(String(200), nullable=True)
