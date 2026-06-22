from pydantic import BaseModel
from typing import Optional, Any

class AuditLogResponse(BaseModel):
    id: str; admin_name: Optional[str] = None; action: str
    target_type: Optional[str] = None; target_id: Optional[str] = None
    details: Optional[str] = None; ip_address: Optional[str] = None
    before_value: Optional[Any] = None; after_value: Optional[Any] = None
    created_at: Optional[str] = None
    class Config: from_attributes = True
