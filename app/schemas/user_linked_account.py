"""
Linked account schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class AddLinkedAccountRequest(BaseModel):
    """Add an external bank account."""
    bank_name: str = Field(..., min_length=1, max_length=200)
    account_number: str = Field(..., min_length=4, max_length=50)
    routing_number: str = Field(..., min_length=9, max_length=20)
    account_type: str = Field(default="checking")


class VerifyMicroDepositsRequest(BaseModel):
    """Verify linked account with micro-deposit amounts."""
    amount_1: float = Field(...)
    amount_2: float = Field(...)


class LinkedAccountResponse(BaseModel):
    """Linked account info."""
    id: str
    bank_name: str
    account_number: str
    routing_number: str
    account_type: str
    is_verified: bool
    is_default: bool
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
