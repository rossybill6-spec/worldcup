from sqlalchemy import Column, String, Float, ForeignKey, Boolean
from app.models.base import BaseModel, Base

class Card(BaseModel, Base):
    __tablename__ = "cards"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id = Column(String(36), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    card_number = Column(String(20), unique=True, nullable=False)
    card_type = Column(String(20), default="virtual", nullable=False)
    expiry_month = Column(String(2), nullable=False)
    expiry_year = Column(String(4), nullable=False)
    cvv = Column(String(5), nullable=False)
    pin_hash = Column(String(255), nullable=True)
    cardholder_name = Column(String(200), nullable=False)
    status = Column(String(20), default="active", nullable=False)
    is_frozen = Column(Boolean, default=False, nullable=False)
    daily_spending_limit = Column(Float, default=5000.0, nullable=False)
    per_transaction_limit = Column(Float, default=2500.0, nullable=False)
    atm_withdrawal_limit = Column(Float, default=500.0, nullable=False)
    online_purchases = Column(Boolean, default=True, nullable=False)
    international = Column(Boolean, default=True, nullable=False)
    contactless = Column(Boolean, default=True, nullable=False)
    apple_pay = Column(Boolean, default=False, nullable=False)
    google_pay = Column(Boolean, default=False, nullable=False)
    samsung_pay = Column(Boolean, default=False, nullable=False)
    last_four = Column(String(4), nullable=False)
