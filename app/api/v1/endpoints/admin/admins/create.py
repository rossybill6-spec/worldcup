from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field, EmailStr
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin import Admin
from app.utils.hashers import hash_user_password
router = APIRouter()

class CreateAdminRequest(BaseModel):
    email: EmailStr; username: str = Field(..., min_length=3, max_length=50)
    full_name: str; password: str = Field(..., min_length=8)
    role_id: str; is_super_admin: bool = False

@router.post("/create", summary="Create admin account")
async def create_admin(data: CreateAdminRequest, db: AsyncSession = Depends(get_db)):
    admin = Admin(email=data.email, username=data.username, full_name=data.full_name,
                  password_hash=hash_user_password(data.password), role_id=data.role_id,
                  is_super_admin=data.is_super_admin)
    db.add(admin); await db.commit()
    return APIResponse(success=True, message="Admin created", data={"id": admin.id})
