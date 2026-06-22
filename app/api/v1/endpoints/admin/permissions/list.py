from fastapi import APIRouter, Depends
from app.constants.permissions import ALL_PERMISSIONS
from app.schemas.common import APIResponse
router = APIRouter()
@router.get("/list", summary="List all available permissions")
async def list_permissions():
    data = [{"key": k, "description": v} for k, v in ALL_PERMISSIONS.items()]
    return APIResponse(success=True, data=data)
