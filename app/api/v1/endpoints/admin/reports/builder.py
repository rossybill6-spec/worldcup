from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.report import GenerateReportRequest
from app.schemas.common import APIResponse
from app.services.report_service import ReportService
router = APIRouter()
@router.post("/generate", summary="Generate a report")
async def generate_report(data: GenerateReportRequest, db: AsyncSession = Depends(get_db)):
    svc = ReportService(db); result = await svc.generate(data.report_type, data.start_date, data.end_date)
    return APIResponse(success=True, message="Report generated", data=result)
