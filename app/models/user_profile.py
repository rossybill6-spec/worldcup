"""
UserProfile model - Extended personal information for each user.
"""

from sqlalchemy import Column, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserProfile(BaseModel, Base):
    """Extended user profile with personal information."""
    
    __tablename__ = "user_profiles"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Personal Info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    ssn_encrypted = Column(String(500), nullable=True)
    ssn_last_four = Column(String(4), nullable=True)
    
    # Address
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    country = Column(String(3), default="US", nullable=False)
    
    # Mailing Address (if different)
    mailing_address_line1 = Column(String(255), nullable=True)
    mailing_address_line2 = Column(String(255), nullable=True)
    mailing_city = Column(String(100), nullable=True)
    mailing_state = Column(String(2), nullable=True)
    mailing_zip_code = Column(String(10), nullable=True)
    
    # Additional
    profile_picture_url = Column(String(500), nullable=True)
    occupation = Column(String(100), nullable=True)
    employer = Column(String(200), nullable=True)
    annual_income = Column(String(50), nullable=True)
    source_of_funds = Column(Text, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile {self.first_name} {self.last_name}>"
