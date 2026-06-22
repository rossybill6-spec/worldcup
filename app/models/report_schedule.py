from sqlalchemy import Column, String, Boolean
from app.models.base import BaseModel, Base

class ReportSchedule(BaseModel, Base):
    __tablename__ = "report_schedules"
    report_type = Column(String(50), nullable=False)
    frequency = Column(String(20), nullable=False)
    recipients = Column(String(500), nullable=True)
    format = Column(String(10), default="csv")
    is_active = Column(Boolean, default=True)
    created_by = Column(String(36), nullable=True)
