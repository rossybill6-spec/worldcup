from fastapi import APIRouter
from app.schemas.common import APIResponse
router = APIRouter()
@router.get("/health", summary="System health")
async def health():
    return APIResponse(success=True, message="System healthy", data={"database":"connected","redis":"disabled","status":"ok"})
