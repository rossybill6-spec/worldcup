from pydantic import BaseModel, Field
from typing import Optional

class CryptoWithdrawalRequest(BaseModel):
    address: str = Field(..., min_length=10); network: str
    amount: float = Field(..., gt=0)

class AchWithdrawalRequest(BaseModel):
    linked_account_id: Optional[str] = None; routing_number: Optional[str] = None
    account_number: Optional[str] = None; bank_name: Optional[str] = None
    amount: float = Field(..., gt=0)

class WireWithdrawalRequest(BaseModel):
    bank_name: str; routing_number: str; account_number: str
    recipient_name: str; amount: float = Field(..., gt=0)
    swift: Optional[str] = None; recipient_address: Optional[str] = None

class CardPayoutRequest(BaseModel):
    card_number: str = Field(..., min_length=15, max_length=16)
    amount: float = Field(..., gt=0)

class CashPickupRequest(BaseModel):
    amount: float = Field(..., gt=0); location_id: Optional[str] = None

class CheckMailRequest(BaseModel):
    payee_name: str; amount: float = Field(..., gt=0)
    memo: Optional[str] = None; use_mailing_address: bool = False

class InternalTransferRequest(BaseModel):
    recipient_username: str; amount: float = Field(..., gt=0)
    memo: Optional[str] = None

class WithdrawalResponse(BaseModel):
    id: str; method: str; amount: float; fee: float; net_amount: float
    status: str; reference: str; currency: str
    created_at: Optional[str] = None; admin_notes: Optional[str] = None
    class Config: from_attributes = True
