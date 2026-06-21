from sqlalchemy import Column, String, Boolean, ForeignKey, Text, JSON
from app.models.base import BaseModel, Base

class Notification(BaseModel, Base):
    __tablename__ = "notifications"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(String(36), nullable=True)
    extra_data = Column(JSON, nullable=True)
