from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.report import GenerateReportRequest
from app.schemas.common import APIResponse
from app.services.report_service import ReportService
router = APIRouter()
@router.post("/save", summary="Generate and save report")
async def save_report(data: GenerateReportRequest, db: AsyncSession = Depends(get_db)):
    svc = ReportService(db); result = await svc.generate(data.report_type, data.start_date, data.end_date)
    r = await svc.save_report(f"{data.report_type}_{data.start_date or 'now'}", data.report_type, "admin", result)
    await db.commit()
    return APIResponse(success=True, message="Report saved", data={"id":r.id})
