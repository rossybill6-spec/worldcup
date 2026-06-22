from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import PlainTextResponse
import csv, io
from app.core.database import get_db
from app.services.audit_service import AuditService
router = APIRouter()
@router.get("/export/csv", summary="Export audit log as CSV")
async def export_audit(db: AsyncSession = Depends(get_db)):
    svc = AuditService(db); result = await svc.get_logs(page=1, per_page=10000)
    output = io.StringIO()
    w = csv.DictWriter(output, fieldnames=["admin_name","action","target_type","target_id","details","ip_address","created_at"])
    w.writeheader()
    for item in result["items"]:
        w.writerow({k: item.get(k) for k in ["admin_name","action","target_type","target_id","details","ip_address","created_at"]})
    return PlainTextResponse(output.getvalue(), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=audit_log.csv"})
