"""
User document schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """KYC document info."""
    id: str
    document_type: str
    file_url: str
    file_name: Optional[str] = None
    verification_status: str
    rejection_reason: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class KYCStatusResponse(BaseModel):
    """KYC verification status."""
    kyc_status: str
    kyc_submitted_at: Optional[str] = None
    kyc_verified_at: Optional[str] = None
    kyc_rejection_reason: Optional[str] = None
    documents: list = []
