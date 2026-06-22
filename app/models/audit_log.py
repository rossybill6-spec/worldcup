from sqlalchemy import Column, String, Text, JSON
from app.models.base import BaseModel, Base

class AuditLog(BaseModel, Base):
    __tablename__ = "audit_logs"
    admin_id = Column(String(36), nullable=True, index=True)
    admin_name = Column(String(200), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    target_type = Column(String(50), nullable=True)
    target_id = Column(String(36), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    before_value = Column(JSON, nullable=True)
    after_value = Column(JSON, nullable=True)
