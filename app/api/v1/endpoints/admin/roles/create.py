from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.admin_role import AdminRole
router = APIRouter()

class CreateRoleRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None; level: str = "3"

@router.post("/create", summary="Create a new role")
async def create_role(data: CreateRoleRequest, db: AsyncSession = Depends(get_db)):
    role = AdminRole(name=data.name, description=data.description, level=data.level)
    db.add(role); await db.commit()
    return APIResponse(success=True, message="Role created", data={"id": role.id, "name": role.name})
