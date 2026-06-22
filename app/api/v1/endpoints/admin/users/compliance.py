from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
router = APIRouter()
@router.get("/{user_id}/compliance", summary="Get user compliance")
async def get_compliance(user_id: str, db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, message="compliance data", data=[])
