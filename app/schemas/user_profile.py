"""
User profile schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field, validator


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

    @validator("state")
    def state_must_be_valid(cls, v):
        if v is None:
            return v
        valid_states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"]
        if v.upper() not in valid_states:
            raise ValueError(f"Invalid US state: {v}")
        return v.upper()


class ProfileResponse(BaseModel):
    """Full user profile."""
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
    occupation: Optional[str] = None
    employer: Optional[str] = None

    class Config:
        from_attributes = True
