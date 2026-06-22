from sqlalchemy import Column, String, Text, JSON
from app.models.base import BaseModel, Base

class Report(BaseModel, Base):
    __tablename__ = "reports"
    name = Column(String(200), nullable=False)
    report_type = Column(String(50), nullable=False)
    parameters = Column(JSON, nullable=True)
    created_by = Column(String(36), nullable=True)
    file_url = Column(String(500), nullable=True)
    format = Column(String(10), default="json")
