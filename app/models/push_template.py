from sqlalchemy import Column, String, Text, Boolean
from app.models.base import BaseModel, Base
class PushTemplate(BaseModel, Base):
    __tablename__ = "push_templates"
    name = Column(String(100), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
