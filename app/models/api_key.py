from sqlalchemy import Column, String, Boolean
from app.models.base import BaseModel, Base
class ApiKey(BaseModel, Base):
    __tablename__ = "api_keys"
    name = Column(String(100), nullable=False)
    key = Column(String(200), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(36), nullable=True)
    last_used_at = Column(String(50), nullable=True)
