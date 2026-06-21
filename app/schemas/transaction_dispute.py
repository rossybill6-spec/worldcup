from pydantic import BaseModel, Field
from typing import Optional

class DisputeRequest(BaseModel):
    transaction_id: str; reason: str = Field(..., min_length=10, max_length=500)

class DisputeResponse(BaseModel):
    id: str; transaction_id: str; reason: str; status: str
    resolution: Optional[str] = None; created_at: Optional[str] = None
    class Config: from_attributes = True
