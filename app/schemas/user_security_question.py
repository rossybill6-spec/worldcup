"""
Security question schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class SecurityQuestionResponse(BaseModel):
    """Security question (answer masked)."""
    id: str
    question_number: int
    question: str

    class Config:
        from_attributes = True


class UpdateSecurityQuestionsRequest(BaseModel):
    """Update security questions."""
    password: str = Field(...)
    question_1: str = Field(..., min_length=1, max_length=500)
    answer_1: str = Field(..., min_length=1, max_length=200)
    question_2: str = Field(..., min_length=1, max_length=500)
    answer_2: str = Field(..., min_length=1, max_length=200)
