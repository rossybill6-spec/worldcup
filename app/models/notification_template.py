from sqlalchemy import Column, String, Text, Boolean
from app.models.base import BaseModel, Base

class NotificationTemplate(BaseModel, Base):
    __tablename__ = "notification_templates"
    name = Column(String(100), unique=True, nullable=False)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    template_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
