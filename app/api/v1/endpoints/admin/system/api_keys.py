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

@router.get("", summary="Get api_keys settings")
async def get_api_keys(db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, data={"configured": True, "type": "api_keys"})

@router.put("", summary="Update api_keys settings")
async def update_api_keys(data: UpdateRequest, db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, message="api_keys updated")
