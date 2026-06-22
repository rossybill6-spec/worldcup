from pydantic import BaseModel
from typing import Optional

class InterestRateResponse(BaseModel):
    id: str; account_type: str; rate: float; min_balance: float
    max_balance: Optional[float] = None; is_enabled: bool; description: Optional[str] = None
    class Config: from_attributes = True

class UpdateInterestRequest(BaseModel):
    rate: Optional[float] = None; min_balance: Optional[float] = None
    max_balance: Optional[float] = None; is_enabled: Optional[bool] = None
