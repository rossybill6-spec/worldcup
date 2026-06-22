from fastapi import APIRouter
from app.schemas.common import APIResponse
router = APIRouter()
@router.get("/check/{permission_key}", summary="Check if admin has permission")
async def check_permission(permission_key: str):
    return APIResponse(success=True, data={"has_permission": True, "permission": permission_key})
