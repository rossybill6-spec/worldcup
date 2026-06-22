from sqlalchemy import Column, String, Float, Boolean
from app.models.base import BaseModel, Base

class FeeSchedule(BaseModel, Base):
    __tablename__ = "fee_schedules"
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    amount = Column(Float, default=0.0)
    fee_type = Column(String(20), default="flat")
    description = Column(String(500), nullable=True)
    is_enabled = Column(Boolean, default=True)
    category = Column(String(50), nullable=True)
