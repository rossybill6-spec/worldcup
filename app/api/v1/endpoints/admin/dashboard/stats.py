from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.admin_service import AdminService
router = APIRouter()
@router.get("/stats", summary="Dashboard statistics")
async def stats(db: AsyncSession = Depends(get_db)):
    svc = AdminService(db); data = await svc.get_dashboard_stats()
    return APIResponse(success=True, message="Dashboard stats", data=data)
