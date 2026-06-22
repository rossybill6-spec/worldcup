from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class AdminLoginRequest(BaseModel):
    email: EmailStr; password: str

class AdminLoginResponse(BaseModel):
    access_token: str; refresh_token: str; token_type: str = "bearer"
    admin_id: str; full_name: str; email: str; role: str; is_super_admin: bool
    permissions: list = []

class AdminCreateRequest(BaseModel):
    email: EmailStr; username: str = Field(..., min_length=3, max_length=50)
    full_name: str; password: str = Field(..., min_length=8)
    role_id: str; is_super_admin: bool = False

class AdminResponse(BaseModel):
    id: str; email: str; username: str; full_name: str
    role_id: Optional[str] = None; is_active: bool; is_super_admin: bool
    last_login_at: Optional[str] = None; created_at: Optional[str] = None
    class Config: from_attributes = True

class DashboardStats(BaseModel):
    total_users: int; active_users: int; total_accounts: int
    pending_deposits: int; pending_withdrawals: int; pending_kyc: int
    total_balance: float; deposits_today: float; withdrawals_today: float
