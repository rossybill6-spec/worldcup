from sqlalchemy import Column, String, Text, Boolean
from app.models.base import BaseModel, Base
class SMSTemplate(BaseModel, Base):
    __tablename__ = "sms_templates"
    name = Column(String(100), unique=True, nullable=False)
    body = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
