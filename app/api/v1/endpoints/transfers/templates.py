from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.transfer import TemplateRequest
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.transfer_service import TransferService
router = APIRouter()
@router.post("/templates", summary="Save transfer template")
async def create_template(data: TemplateRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = TransferService(db); r = await svc.create_template(user.id, data.model_dump(exclude_none=True))
    await db.commit()
    return APIResponse(success=True, message="Template saved", data=r)
@router.get("/templates", summary="List templates")
async def list_templates(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = TransferService(db); templates = await svc.get_templates(user.id)
    return APIResponse(success=True, message="Templates retrieved", data=templates)
@router.delete("/templates/{template_id}", summary="Delete template")
async def delete_template(template_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = TransferService(db); ok = await svc.delete_template(user.id, template_id)
    await db.commit()
    return APIResponse(success=ok, message="Template deleted" if ok else "Not found")
