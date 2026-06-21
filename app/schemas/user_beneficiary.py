"""
Beneficiary schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class CreateBeneficiaryRequest(BaseModel):
    """Add a new beneficiary."""
    name: str = Field(..., min_length=1, max_length=200)
    account_number: str = Field(..., min_length=4, max_length=50)
    routing_number: Optional[str] = Field(None, max_length=20)
    bank_name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    relationship: Optional[str] = Field(None, max_length=50)
    nickname: Optional[str] = Field(None, max_length=100)


class UpdateBeneficiaryRequest(BaseModel):
    """Update a beneficiary."""
    name: Optional[str] = Field(None, max_length=200)
    account_number: Optional[str] = Field(None, max_length=50)
    routing_number: Optional[str] = Field(None, max_length=20)
    bank_name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    relationship: Optional[str] = Field(None, max_length=50)
    nickname: Optional[str] = Field(None, max_length=100)


class BeneficiaryResponse(BaseModel):
    """Beneficiary info."""
    id: str
    name: str
    account_number: str
    routing_number: Optional[str] = None
    bank_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    relationship: Optional[str] = None
    nickname: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
