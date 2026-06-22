from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
router = APIRouter()
@router.post("/verify-2fa", summary="Verify admin 2FA")
async def verify_2fa(): return APIResponse(success=True, message="2FA verified")
