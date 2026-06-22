from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.system_setting import SystemSetting
router = APIRouter()

class UpdateSettingRequest(BaseModel):
    key: str; value: str; description: Optional[str] = None

@router.get("", summary="Get all system settings")
async def get_settings(db: AsyncSession = Depends(get_db)):
    settings = (await db.execute(select(SystemSetting))).scalars().all()
    return APIResponse(success=True, data={s.key: s.value for s in settings})

@router.put("", summary="Update system setting")
async def update_setting(data: UpdateSettingRequest, db: AsyncSession = Depends(get_db)):
    s = (await db.execute(select(SystemSetting).where(SystemSetting.key == data.key))).scalar_one_or_none()
    if s: s.value = data.value
    else: db.add(SystemSetting(key=data.key, value=data.value, description=data.description))
    await db.commit()
    return APIResponse(success=True, message=f"{data.key} updated")
