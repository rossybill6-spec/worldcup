from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.email_template import EmailTemplate
router = APIRouter()

class UpdateEmailTemplateRequest(BaseModel):
    subject: Optional[str] = None; body: Optional[str] = None; is_active: Optional[bool] = None

@router.get("", summary="List email templates")
async def list_templates(db: AsyncSession = Depends(get_db)):
    temps = (await db.execute(select(EmailTemplate))).scalars().all()
    return APIResponse(success=True, data=[{"id":t.id,"name":t.name,"subject":t.subject,"is_active":t.is_active} for t in temps])

@router.put("/{template_id}", summary="Update email template")
async def update_template(template_id: str, data: UpdateEmailTemplateRequest, db: AsyncSession = Depends(get_db)):
    t = (await db.execute(select(EmailTemplate).where(EmailTemplate.id == template_id))).scalar_one_or_none()
    if not t: return APIResponse(success=False, message="Not found")
    for k,v in data.model_dump(exclude_none=True).items(): setattr(t, k, v)
    await db.commit()
    return APIResponse(success=True, message="Template updated")
