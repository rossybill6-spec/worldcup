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

@router.get("", summary="Get kyc_settings settings")
async def get_kyc_settings(db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, data={"configured": True, "type": "kyc_settings"})

@router.put("", summary="Update kyc_settings settings")
async def update_kyc_settings(data: UpdateRequest, db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, message="kyc_settings updated")
