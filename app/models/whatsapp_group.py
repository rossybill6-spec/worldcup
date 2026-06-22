from sqlalchemy import Column, String, Text
from app.models.base import BaseModel, Base
class WhatsAppGroup(BaseModel, Base):
    __tablename__ = "whatsapp_groups"
    name = Column(String(200), nullable=False)
    invite_link = Column(Text, nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(String(5), default="true")
