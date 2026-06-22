from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.report_service import ReportService
router = APIRouter()
@router.get("/list", summary="List saved reports")
async def list_reports(db: AsyncSession = Depends(get_db)):
    svc = ReportService(db); reports = await svc.get_reports()
    data = [{"id":r.id,"name":r.name,"report_type":r.report_type,"format":r.format,"created_at":r.created_at.isoformat() if r.created_at else None} for r in reports]
    return APIResponse(success=True, data=data)
