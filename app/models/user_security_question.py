"""
UserSecurityQuestion model - Account recovery questions.
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, Base


class UserSecurityQuestion(BaseModel, Base):
    """Security questions for password reset and account recovery."""
    
    __tablename__ = "user_security_questions"
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Question and answer
    question_number = Column(Integer, nullable=False)
    question = Column(String(500), nullable=False)
    answer_hash = Column(String(255), nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="security_questions")
    
    def __repr__(self):
        return f"<UserSecurityQuestion {self.question_number} for {self.user_id}>"
