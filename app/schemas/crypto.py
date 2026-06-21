"""Crypto schemas."""
from pydantic import BaseModel
from typing import Optional

class CryptoNetworkResponse(BaseModel):
    id: str; name: str; symbol: str; slug: str; network_type: str
    admin_wallet_address: str; min_confirmations: str; is_enabled: bool
    block_explorer_url: Optional[str] = None; icon: Optional[str] = None
    class Config: from_attributes = True
