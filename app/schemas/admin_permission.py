from pydantic import BaseModel
from typing import List, Optional

class AssignPermissionsRequest(BaseModel):
    role_id: str; permissions: List[str]

class PermissionResponse(BaseModel):
    id: str; role_id: str; permission_key: str; category: Optional[str] = None
    class Config: from_attributes = True
