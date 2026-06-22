from pydantic import BaseModel
from typing import Optional

class FeeResponse(BaseModel):
    id: str; name: str; slug: str; amount: float; fee_type: str
    description: Optional[str] = None; is_enabled: bool; category: Optional[str] = None
    class Config: from_attributes = True

class UpdateFeeRequest(BaseModel):
    amount: Optional[float] = None; is_enabled: Optional[bool] = None
    description: Optional[str] = None
