from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin import Admin
router = APIRouter()

class EditAdminRequest(BaseModel):
    full_name: Optional[str] = None; is_active: Optional[bool] = None
    role_id: Optional[str] = None

@router.put("/{admin_id}", summary="Edit admin")
async def edit_admin(admin_id: str, data: EditAdminRequest, db: AsyncSession = Depends(get_db)):
    a = (await db.execute(select(Admin).where(Admin.id == admin_id))).scalar_one_or_none()
    if not a: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(a, k, v)
    await db.commit()
    return APIResponse(success=True, message="Admin updated")
