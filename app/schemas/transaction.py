from pydantic import BaseModel
from typing import Optional

class TransactionResponse(BaseModel):
    id: str; transaction_type: str; amount: float; fee: float; net_amount: float
    currency: str; status: str; reference: Optional[str] = None
    description: Optional[str] = None; source: Optional[str] = None
    recipient: Optional[str] = None; category: Optional[str] = None
    created_at: Optional[str] = None
    class Config: from_attributes = True

class TransactionFilter(BaseModel):
    transaction_type: Optional[str] = None; status: Optional[str] = None
    start_date: Optional[str] = None; end_date: Optional[str] = None
    min_amount: Optional[float] = None; max_amount: Optional[float] = None
    search: Optional[str] = None; sort_by: str = "created_at"
    sort_order: str = "desc"
