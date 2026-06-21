from pydantic import BaseModel, Field
from typing import Optional

class NotificationResponse(BaseModel):
    id: str; title: str; message: str; notification_type: str
    is_read: bool; reference_type: Optional[str] = None
    reference_id: Optional[str] = None; created_at: Optional[str] = None
    class Config: from_attributes = True

class NotificationPreferencesUpdate(BaseModel):
    push_enabled: Optional[bool] = None; email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
