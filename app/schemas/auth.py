"""
Authentication schemas - Signup, login, tokens, 2FA, password reset.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


# ============ SIGNUP ============

class SignupRequest(BaseModel):
    """Request body for user registration."""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(...)
    phone: str = Field(..., min_length=10, max_length=20)
    date_of_birth: str = Field(...)
    ssn: str = Field(..., min_length=9, max_length=11)
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    zip_code: str = Field(..., min_length=5, max_length=10)
    username: str = Field(..., min_length=4, max_length=30)
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)
    security_question_1: str = Field(..., min_length=1, max_length=500)
    security_answer_1: str = Field(..., min_length=1, max_length=200)
    security_question_2: str = Field(..., min_length=1, max_length=500)
    security_answer_2: str = Field(..., min_length=1, max_length=200)
    agree_to_terms: bool = Field(..., description="Must be true")

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("state")
    def state_must_be_valid(cls, v):
        valid_states = [
            "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
            "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
            "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
            "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
            "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY",
            "DC","AS","GU","MP","PR","VI",
        ]
        if v.upper() not in valid_states:
            raise ValueError(f"Invalid US state: {v}")
        return v.upper()

    @validator("agree_to_terms")
    def must_agree(cls, v):
        if not v:
            raise ValueError("You must agree to the Terms of Service")
        return v


class SignupResponse(BaseModel):
    """Response after successful signup."""
    user_id: str
    email: str
    username: str
    message: str = "Account created. Please verify your email."


# ============ LOGIN ============

class LoginRequest(BaseModel):
    """Request body for login."""
    login: str = Field(..., description="Email or username")
    password: str = Field(...)
    device_name: Optional[str] = Field(None)
    device_type: Optional[str] = Field(None)


class LoginResponse(BaseModel):
    """Response after successful login."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    requires_2fa: bool = False
    session_id: str


class TokenRefreshRequest(BaseModel):
    """Request body for refreshing tokens."""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Response with new token pair."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# ============ VERIFICATION ============

class VerifyEmailRequest(BaseModel):
    """Request body for email verification."""
    email: EmailStr = Field(...)
    code: str = Field(..., min_length=6, max_length=6)


class VerifyPhoneRequest(BaseModel):
    """Request body for phone verification."""
    code: str = Field(..., min_length=6, max_length=6)


class ResendVerificationRequest(BaseModel):
    """Request to resend verification code."""
    email: EmailStr = Field(...)


# ============ PASSWORD RESET ============

class ForgotPasswordRequest(BaseModel):
    """Request body for forgot password."""
    email: EmailStr = Field(...)


class ResetPasswordRequest(BaseModel):
    """Request body for password reset."""
    token: str = Field(...)
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


class ForgotUsernameRequest(BaseModel):
    """Request body for forgot username."""
    email: EmailStr = Field(...)


class ChangePasswordRequest(BaseModel):
    """Request body for changing password (when logged in)."""
    current_password: str = Field(...)
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("Passwords do not match")
        return v


# ============ 2FA ============

class Setup2FAResponse(BaseModel):
    """Response with 2FA setup details."""
    secret: str
    qr_code_url: str
    manual_key: str
    message: str


class Verify2FARequest(BaseModel):
    """Request body for verifying 2FA code."""
    code: str = Field(..., min_length=6, max_length=6)
    trust_device: bool = False
    device_name: Optional[str] = None
    device_type: Optional[str] = None


class Verify2FAResponse(BaseModel):
    """Response after successful 2FA verification."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    trusted_device_id: Optional[str] = None


class Enable2FARequest(BaseModel):
    """Request to enable 2FA."""
    method: str = Field(..., description="sms, authenticator, or email")
    phone_number: Optional[str] = None


class Disable2FARequest(BaseModel):
    """Request to disable 2FA."""
    code: str = Field(..., min_length=6, max_length=6)
    password: str = Field(...)


# ============ BIOMETRIC ============

class BiometricSetupRequest(BaseModel):
    """Request to enable biometric login."""
    biometric_token: str = Field(...)
    device_name: str = Field(...)
    device_type: Optional[str] = None


class BiometricLoginRequest(BaseModel):
    """Request to login with biometric."""
    biometric_token: str = Field(...)


# ============ USER BRIEF ============

class UserBriefResponse(BaseModel):
    """Brief user info returned with tokens."""
    id: str
    email: str
    username: str
    first_name: str
    last_name: str
    is_email_verified: bool
    is_phone_verified: bool
    kyc_status: str

    class Config:
        from_attributes = True
