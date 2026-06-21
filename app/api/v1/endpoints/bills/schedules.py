from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.bill_service import BillService
router = APIRouter()
@router.get("/schedules", summary="List scheduled payments")
async def list_schedules(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); schedules = await svc.get_schedules(user.id)
    return APIResponse(success=True, message="Schedules retrieved", data=schedules)
@router.delete("/schedules/{schedule_id}", summary="Cancel scheduled payment")
async def cancel_schedule(schedule_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = BillService(db); ok = await svc.cancel_schedule(user.id, schedule_id)
    await db.commit(); return APIResponse(success=ok, message="Schedule cancelled" if ok else "Not found")
