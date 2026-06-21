"""
UserBeneficiary model - Saved transfer beneficiaries.
"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserBeneficiary(BaseModel, Base):
    """Saved beneficiaries for transfers."""
    
    __tablename__ = "user_beneficiaries"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(200), nullable=False)
    account_number = Column(String(50), nullable=False)
    routing_number = Column(String(20), nullable=True)
    bank_name = Column(String(200), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    relationship = Column(String(50), nullable=True)
    nickname = Column(String(100), nullable=True)
    
    def __repr__(self):
        return f"<UserBeneficiary {self.name}>"
