from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from app.models.base import BaseModel, Base

class AlertPreference(BaseModel, Base):
    __tablename__ = "alert_preferences"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    balance_low = Column(Boolean, default=False)
    balance_low_threshold = Column(Float, default=100.0)
    balance_high = Column(Boolean, default=False)
    balance_high_threshold = Column(Float, default=10000.0)
    large_deposit = Column(Boolean, default=True)
    large_deposit_threshold = Column(Float, default=1000.0)
    large_withdrawal = Column(Boolean, default=True)
    large_withdrawal_threshold = Column(Float, default=500.0)
    security_login = Column(Boolean, default=True)
    security_password_change = Column(Boolean, default=True)
    weekly_summary = Column(Boolean, default=False)
    monthly_summary = Column(Boolean, default=False)
