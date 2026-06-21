from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import PlainTextResponse
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.export_service import ExportService
router = APIRouter()

@router.get("/transactions/csv", summary="Export transactions as CSV", response_class=PlainTextResponse)
async def export_csv(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = ExportService(db); csv_data = await svc.export_csv(user.id)
    return PlainTextResponse(content=csv_data, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=transactions.csv"})
