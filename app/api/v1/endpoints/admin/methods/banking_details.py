from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.system_config import SystemConfig
router = APIRouter()

class BankingDetailsRequest(BaseModel):
    bank_name: Optional[str] = None; routing_number: Optional[str] = None
    account_number: Optional[str] = None; swift_code: Optional[str] = None
    bank_address: Optional[str] = None; wire_instructions: Optional[str] = None

@router.get("/banking", summary="Get banking details")
async def get_banking(db: AsyncSession = Depends(get_db)):
    configs = (await db.execute(select(SystemConfig).where(SystemConfig.key.like("bank_%")))).scalars().all()
    data = {c.key: c.value for c in configs}
    return APIResponse(success=True, data=data)

@router.put("/banking", summary="Update banking details")
async def update_banking(data: BankingDetailsRequest, db: AsyncSession = Depends(get_db)):
    for k, v in data.model_dump(exclude_none=True).items():
        key = f"bank_{k}"
        cfg = (await db.execute(select(SystemConfig).where(SystemConfig.key == key))).scalar_one_or_none()
        if cfg: cfg.value = v
        else: db.add(SystemConfig(key=key, value=v, description=f"Banking: {k}"))
    await db.commit()
    return APIResponse(success=True, message="Banking details updated")
