from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.admin import AdminLoginRequest
from app.schemas.common import APIResponse
from app.services.admin_service import AdminService
router = APIRouter()
@router.post("/login", summary="Admin login")
async def login(data: AdminLoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    svc = AdminService(db); r = await svc.login(data.email, data.password, request.client.host if request.client else None, request.headers.get("user-agent"))
    if not r.get("success"): return APIResponse(success=False, message=r.get("message"))
    await db.commit(); return APIResponse(success=True, message="Login successful", data=r)
