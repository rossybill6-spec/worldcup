from sqlalchemy import Column, String
from app.models.base import BaseModel, Base

class AdminPermission(BaseModel, Base):
    __tablename__ = "admin_permissions"
    role_id = Column(String(36), nullable=False, index=True)
    permission_key = Column(String(200), nullable=False)
    category = Column(String(100), nullable=True)
