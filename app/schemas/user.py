"""
User schemas - Profile, security settings, and user management.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserProfileResponse(BaseModel):
    """Full user profile response."""
    id: str
    email: str
    username: str
    phone: Optional[str] = None
    is_email_verified: bool
    is_phone_verified: bool
    is_2fa_enabled: bool
    biometric_enabled: bool
    kyc_status: str
    is_active: bool
    last_login_at: Optional[str] = None
    created_at: Optional[str] = None

    # Profile
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    ssn_last_four: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    profile_picture_url: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    """Request to update user profile."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    address_line1: Optional[str] = Field(None, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    zip_code: Optional[str] = Field(None, min_length=5, max_length=10)
    occupation: Optional[str] = Field(None, max_length=100)
    employer: Optional[str] = Field(None, max_length=200)


class UpdateEmailRequest(BaseModel):
    """Request to change email."""
    new_email: EmailStr = Field(...)
    password: str = Field(...)


class UpdatePhoneRequest(BaseModel):
    """Request to change phone."""
    new_phone: str = Field(..., min_length=10, max_length=20)
    password: str = Field(...)


class SessionResponse(BaseModel):
    """User session info."""
    id: str
    ip_address: Optional[str] = None
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    location: Optional[str] = None
    is_active: bool
    created_at: Optional[str] = None
    expires_at: Optional[str] = None

    class Config:
        from_attributes = True


class DeviceResponse(BaseModel):
    """Trusted device info."""
    id: str
    device_name: str
    device_type: Optional[str] = None
    is_trusted: bool
    last_used_at: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class LoginHistoryResponse(BaseModel):
    """Login history entry."""
    id: str
    login_method: str
    ip_address: Optional[str] = None
    device_info: Optional[str] = None
    location: Optional[str] = None
    is_successful: bool
    failure_reason: Optional[str] = None
    attempted_at: Optional[str] = None

    class Config:
        from_attributes = True


class ActivityLogResponse(BaseModel):
    """Activity log entry."""
    id: str
    action: str
    description: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
