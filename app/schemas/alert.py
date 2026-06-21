from pydantic import BaseModel
from typing import Optional

class AlertPreferenceResponse(BaseModel):
    balance_low: bool; balance_low_threshold: float
    balance_high: bool; balance_high_threshold: float
    large_deposit: bool; large_deposit_threshold: float
    large_withdrawal: bool; large_withdrawal_threshold: float
    security_login: bool; security_password_change: bool
    weekly_summary: bool; monthly_summary: bool
    class Config: from_attributes = True

class AlertPreferenceUpdate(BaseModel):
    balance_low: Optional[bool] = None; balance_low_threshold: Optional[float] = None
    balance_high: Optional[bool] = None; balance_high_threshold: Optional[float] = None
    large_deposit: Optional[bool] = None; large_deposit_threshold: Optional[float] = None
    large_withdrawal: Optional[bool] = None; large_withdrawal_threshold: Optional[float] = None
    security_login: Optional[bool] = None; security_password_change: Optional[bool] = None
    weekly_summary: Optional[bool] = None; monthly_summary: Optional[bool] = None
