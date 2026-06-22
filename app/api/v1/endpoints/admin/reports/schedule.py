from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.report import ScheduleReportRequest
from app.schemas.common import APIResponse
from app.services.report_service import ReportService
router = APIRouter()
@router.post("/schedule", summary="Schedule a report")
async def schedule_report(data: ScheduleReportRequest, db: AsyncSession = Depends(get_db)):
    svc = ReportService(db); s = await svc.schedule(data.report_type, data.frequency, data.recipients, data.format, "admin")
    await db.commit()
    return APIResponse(success=True, message=f"Report scheduled {data.frequency}", data={"id":s.id})
