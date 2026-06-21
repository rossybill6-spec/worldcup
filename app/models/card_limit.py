from sqlalchemy import Column, String, Float, ForeignKey
from app.models.base import BaseModel, Base

class CardLimit(BaseModel, Base):
    __tablename__ = "card_limits"
    card_id = Column(String(36), ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    daily_spending = Column(Float, default=5000.0, nullable=False)
    per_transaction = Column(Float, default=2500.0, nullable=False)
    atm_withdrawal = Column(Float, default=500.0, nullable=False)
