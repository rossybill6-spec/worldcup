from pydantic import BaseModel, Field
from typing import Optional

class CreatePayeeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    account_number: Optional[str] = None; address: Optional[str] = None
    phone: Optional[str] = None; category: Optional[str] = None
    nickname: Optional[str] = None

class UpdatePayeeRequest(BaseModel):
    name: Optional[str] = None; account_number: Optional[str] = None
    address: Optional[str] = None; phone: Optional[str] = None
    category: Optional[str] = None; nickname: Optional[str] = None

class PayeeResponse(BaseModel):
    id: str; name: str; account_number: Optional[str] = None
    category: Optional[str] = None; nickname: Optional[str] = None
    class Config: from_attributes = True

class MakePaymentRequest(BaseModel):
    payee_id: str; account_id: str
    amount: float = Field(..., gt=0); scheduled_date: Optional[str] = None
    is_recurring: bool = False; frequency: Optional[str] = None
    memo: Optional[str] = None

class PaymentResponse(BaseModel):
    id: str; amount: float; fee: float; status: str; reference: str
    scheduled_date: Optional[str] = None; is_recurring: bool
    memo: Optional[str] = None; created_at: Optional[str] = None
    class Config: from_attributes = True

class ScheduleResponse(BaseModel):
    id: str; payee_name: Optional[str] = None; amount: float
    frequency: str; next_payment_date: Optional[str] = None
    is_active: bool
    class Config: from_attributes = True
