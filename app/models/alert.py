from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from app.models.base import BaseModel, Base

class Alert(BaseModel, Base):
    __tablename__ = "alerts"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)
    threshold = Column(Float, nullable=True)
    is_enabled = Column(Boolean, default=True)
    last_triggered_at = Column(String(50), nullable=True)
