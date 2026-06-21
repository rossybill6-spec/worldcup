"""Deposit schemas."""
from pydantic import BaseModel, Field
from typing import Optional

class CryptoDepositInitiateRequest(BaseModel):
    amount: float = Field(..., gt=0)
    network: str = Field(..., description="btc, eth, usdc_erc20, usdt_trc20")

class CryptoDepositInitiateResponse(BaseModel):
    session_id: str; reference: str; address: str; network: str
    expected_amount: float; qr_code: Optional[str] = None
    deep_link: Optional[str] = None; expires_at: str

class AchDepositRequest(BaseModel):
    account_id: str; linked_account_id: Optional[str] = None
    routing_number: Optional[str] = None; account_number: Optional[str] = None
    bank_name: Optional[str] = None; amount: float = Field(..., gt=0)

class WireDepositRequest(BaseModel):
    amount: float = Field(..., gt=0); sending_bank_name: Optional[str] = None

class CheckDepositRequest(BaseModel):
    account_id: str; amount: float = Field(..., gt=0)

class CashDepositRequest(BaseModel):
    amount: float = Field(..., gt=0); location_id: Optional[str] = None

class DirectDepositRequest(BaseModel):
    account_id: str; employer_name: Optional[str] = None

class P2PDepositRequest(BaseModel):
    from_username: str; amount: float = Field(..., gt=0); memo: Optional[str] = None

class DepositResponse(BaseModel):
    id: str; method: str; amount: float; fee: float; net_amount: float
    status: str; reference: str; currency: str
    created_at: Optional[str] = None; admin_notes: Optional[str] = None
    class Config: from_attributes = True
