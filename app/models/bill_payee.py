from sqlalchemy import Column, String, ForeignKey, Text
from app.models.base import BaseModel, Base

class BillPayee(BaseModel, Base):
    __tablename__ = "bill_payees"
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    account_number = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    category = Column(String(50), nullable=True)
    nickname = Column(String(100), nullable=True)
