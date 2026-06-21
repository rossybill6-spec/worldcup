from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.export_service import ExportService
router = APIRouter()
@router.get("/transactions/json", summary="Export transactions as JSON")
async def export_json(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = ExportService(db); data = await svc.export_json(user.id)
    return APIResponse(success=True, message="Export ready", data=data)
