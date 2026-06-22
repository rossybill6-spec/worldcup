from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
router = APIRouter()
@router.post("/refresh", summary="Refresh admin token")
async def refresh(): return APIResponse(success=True, message="Token refreshed")
