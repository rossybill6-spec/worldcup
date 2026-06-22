from pydantic import BaseModel, Field
from typing import Optional

class CreateRoleRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None; level: str = "3"

class RoleResponse(BaseModel):
    id: str; name: str; description: Optional[str] = None
    level: str; created_at: Optional[str] = None
    class Config: from_attributes = True
