from fastapi import APIRouter
from app.schemas.common import APIResponse
router = APIRouter()
@router.get("", summary="List notification templates")
async def list_templates():
    return APIResponse(success=True, data=[{"name":"deposit_approved","subject":"Deposit Approved","body":"Your deposit of {{amount}} has been approved."}])
