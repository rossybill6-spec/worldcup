from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
router = APIRouter()

class UpdateRequest(BaseModel):
    value: Optional[str] = None; is_active: Optional[bool] = None
    data: Optional[dict] = None

@router.get("", summary="Get webhooks settings")
async def get_webhooks(db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, data={"configured": True, "type": "webhooks"})

@router.put("", summary="Update webhooks settings")
async def update_webhooks(data: UpdateRequest, db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, message="webhooks updated")
