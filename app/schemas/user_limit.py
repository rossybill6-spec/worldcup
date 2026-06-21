"""
User limit schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class LimitResponse(BaseModel):
    """User account limits."""
    daily_deposit_limit: Optional[float] = 10000.0
    daily_withdrawal_limit: Optional[float] = 5000.0
    daily_transfer_limit: Optional[float] = 10000.0
    per_transaction_limit: Optional[float] = 5000.0
    monthly_deposit_limit: Optional[float] = 50000.0
    monthly_withdrawal_limit: Optional[float] = 25000.0
    card_spending_limit: Optional[float] = 5000.0
    atm_withdrawal_limit: Optional[float] = 500.0


class RequestLimitIncreaseRequest(BaseModel):
    """Request a limit increase."""
    limit_type: str = Field(..., description="daily_deposit, daily_withdrawal, etc.")
    requested_amount: float = Field(..., gt=0)
    reason: Optional[str] = Field(None, max_length=500)
