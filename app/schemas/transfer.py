from pydantic import BaseModel, Field
from typing import Optional

class InternalTransferRequest(BaseModel):
    from_account_id: str; to_account_id: str
    amount: float = Field(..., gt=0); memo: Optional[str] = None

class ExternalTransferRequest(BaseModel):
    from_account_id: str; amount: float = Field(..., gt=0)
    recipient_name: str; recipient_account: str; recipient_routing: str
    recipient_bank: Optional[str] = None; memo: Optional[str] = None

class WireTransferRequest(BaseModel):
    from_account_id: str; amount: float = Field(..., gt=0)
    recipient_name: str; recipient_account: str; recipient_routing: str
    recipient_bank: str; swift_code: Optional[str] = None
    recipient_address: Optional[str] = None; memo: Optional[str] = None

class InternationalTransferRequest(BaseModel):
    from_account_id: str; amount: float = Field(..., gt=0)
    recipient_name: str; recipient_account: str
    recipient_bank: str; swift_code: str; country: str
    currency: str = "USD"; memo: Optional[str] = None

class TemplateRequest(BaseModel):
    name: str; transfer_type: str; from_account_id: str
    amount: float = Field(..., gt=0); to_account_id: Optional[str] = None
    recipient_name: Optional[str] = None; recipient_account: Optional[str] = None
    recipient_routing: Optional[str] = None; recipient_bank: Optional[str] = None
    swift_code: Optional[str] = None; memo: Optional[str] = None
    frequency: Optional[str] = None

class TransferResponse(BaseModel):
    id: str; transfer_type: str; amount: float; fee: float; net_amount: float
    status: str; reference: str; currency: str
    recipient_name: Optional[str] = None; memo: Optional[str] = None
    created_at: Optional[str] = None
    class Config: from_attributes = True

class TemplateResponse(BaseModel):
    id: str; name: str; transfer_type: str; amount: float
    frequency: Optional[str] = None; is_active: bool
    class Config: from_attributes = True
