from pydantic import BaseModel
from typing import Optional
class WithdrawalMethodResponse(BaseModel):
    id: str; name: str; slug: str; description: Optional[str] = None
    is_enabled: bool; min_amount: float; max_amount: float
    fee_type: str; fee_amount: float; processing_time: Optional[str] = None
    icon: Optional[str] = None
    class Config: from_attributes = True
