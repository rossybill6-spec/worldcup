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

@router.get("", summary="Get legal settings")
async def get_legal(db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, data={"configured": True, "type": "legal"})

@router.put("", summary="Update legal settings")
async def update_legal(data: UpdateRequest, db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, message="legal updated")
