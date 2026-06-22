from sqlalchemy import Column, String, Text, Boolean
from app.models.base import BaseModel, Base
class Announcement(BaseModel, Base):
    __tablename__ = "announcements"
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String(20), default="normal")
    is_published = Column(Boolean, default=False)
    created_by = Column(String(36), nullable=True)
