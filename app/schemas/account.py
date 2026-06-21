"""
Account schemas.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class AccountResponse(BaseModel):
    """Account info response."""
    id: str
    account_number: str
    account_type: str
    account_name: Optional[str] = None
    balance: float
    available_balance: float
    pending_balance: float
    currency: str
    is_active: bool
    is_frozen: bool
    interest_rate: float
    overdraft_protection: bool
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class CreateSavingsRequest(BaseModel):
    """Request to create a savings account."""
    account_name: Optional[str] = Field(None, max_length=100)
    initial_deposit: float = Field(default=0.0, ge=0.0)


class BalanceResponse(BaseModel):
    """Balance breakdown."""
    account_id: str
    account_number: str
    account_type: str
    balance: float
    available_balance: float
    pending_balance: float


class StatementResponse(BaseModel):
    """Account statement info."""
    id: str
    statement_date: str
    period_start: str
    period_end: str
    opening_balance: float
    closing_balance: float
    total_deposits: float
    total_withdrawals: float
    total_fees: float
    interest_earned: float
    file_url: Optional[str] = None

    class Config:
        from_attributes = True


class AccountsListResponse(BaseModel):
    """List of user's accounts."""
    accounts: List[AccountResponse]
    total_balance: float
