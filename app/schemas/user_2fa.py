"""
2FA schemas.
"""

from typing import Optional
from pydantic import BaseModel


class TwoFAMethodResponse(BaseModel):
    """2FA method info."""
    id: str
    method_type: str
    is_enabled: bool
    is_default: bool
    phone_number: Optional[str] = None
    enabled_at: Optional[str] = None

    class Config:
        from_attributes = True


class TwoFAStatusResponse(BaseModel):
    """Overall 2FA status."""
    is_2fa_enabled: bool
    methods: list = []
