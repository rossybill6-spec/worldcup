from sqlalchemy import Column, String, Float, Boolean
from app.models.base import BaseModel, Base

class InterestRate(BaseModel, Base):
    __tablename__ = "interest_rates"
    account_type = Column(String(50), nullable=False)
    rate = Column(Float, default=0.0)
    min_balance = Column(Float, default=0.0)
    max_balance = Column(Float, nullable=True)
    is_enabled = Column(Boolean, default=True)
    description = Column(String(200), nullable=True)
