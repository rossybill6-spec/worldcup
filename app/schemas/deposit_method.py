"""Deposit method schemas."""
from pydantic import BaseModel
from typing import Optional

class DepositMethodResponse(BaseModel):
    id: str; name: str; slug: str; description: Optional[str] = None
    is_enabled: bool; min_amount: float; max_amount: float
    fee_type: str; fee_amount: float; processing_time: Optional[str] = None
    instructions: Optional[str] = None; icon: Optional[str] = None
    class Config: from_attributes = True
