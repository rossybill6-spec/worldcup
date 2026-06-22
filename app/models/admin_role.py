from sqlalchemy import Column, String, Text
from app.models.base import BaseModel, Base

class AdminRole(BaseModel, Base):
    __tablename__ = "admin_roles"
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    level = Column(String(10), default="3")
    is_system = Column(String(5), default="false")
