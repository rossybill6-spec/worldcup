from sqlalchemy import Column, String, Text, Boolean
from app.models.base import BaseModel, Base
class EmailTemplate(BaseModel, Base):
    __tablename__ = "email_templates"
    name = Column(String(100), unique=True, nullable=False)
    subject = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
