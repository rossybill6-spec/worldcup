from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.services.audit_service import AuditService
router = APIRouter()
@router.get("/list", summary="View audit log")
async def audit_list(
    admin_id: Optional[str] = None, action: Optional[str] = None,
    page: int = Query(1, ge=1), per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    svc = AuditService(db); result = await svc.get_logs(admin_id, action, page, per_page)
    return APIResponse(success=True, data=result)
