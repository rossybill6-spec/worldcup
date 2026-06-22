from sqlalchemy import Column, String, Boolean, Text
from app.models.base import BaseModel, Base
class Webhook(BaseModel, Base):
    __tablename__ = "webhooks"
    name = Column(String(100), nullable=False)
    url = Column(Text, nullable=False)
    event_type = Column(String(100), nullable=False)
    secret = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
