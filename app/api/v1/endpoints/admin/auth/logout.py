from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
router = APIRouter()
@router.post("/logout", summary="Admin logout")
async def logout(): return APIResponse(success=True, message="Logged out")
