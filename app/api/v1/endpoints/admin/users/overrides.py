from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
router = APIRouter()
@router.get("/{user_id}/overrides", summary="Get user overrides")
async def get_overrides(user_id: str, db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, message="overrides data", data=[])
