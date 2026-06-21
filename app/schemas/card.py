from pydantic import BaseModel, Field
from typing import Optional

class CardResponse(BaseModel):
    id: str; card_type: str; card_number_masked: str; expiry_month: str
    expiry_year: str; cardholder_name: str; status: str; is_frozen: bool
    daily_spending_limit: float; online_purchases: bool; international: bool
    contactless: bool; apple_pay: bool; google_pay: bool; samsung_pay: bool
    last_four: str; created_at: Optional[str] = None
    class Config: from_attributes = True

class CardLimitsRequest(BaseModel):
    daily_spending_limit: Optional[float] = None
    per_transaction_limit: Optional[float] = None
    atm_withdrawal_limit: Optional[float] = None

class CardSettingsRequest(BaseModel):
    online_purchases: Optional[bool] = None
    international: Optional[bool] = None
    contactless: Optional[bool] = None

class PinRequest(BaseModel):
    pin: str = Field(..., min_length=4, max_length=4)

class ActivateCardRequest(BaseModel):
    last_four: str = Field(..., min_length=4, max_length=4)

class DigitalWalletRequest(BaseModel):
    wallet_type: str = Field(..., description="apple_pay, google_pay, samsung_pay")

class CardDisputeRequest(BaseModel):
    transaction_id: str; reason: str = Field(..., min_length=10, max_length=500)

class CardTransactionResponse(BaseModel):
    id: str; amount: float; merchant: Optional[str] = None
    category: Optional[str] = None; status: str; transaction_type: str
    reference: Optional[str] = None; location: Optional[str] = None
    created_at: Optional[str] = None
    class Config: from_attributes = True
