from sqlalchemy import Column, String, Text
from app.models.base import BaseModel, Base

class SystemConfig(BaseModel, Base):
    __tablename__ = "system_configs"
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text, nullable=True)
    description = Column(String(500), nullable=True)
