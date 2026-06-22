from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.crypto_network import CryptoNetwork
router = APIRouter()

class UpdateCryptoRequest(BaseModel):
    name: Optional[str] = None; symbol: Optional[str] = None
    admin_wallet_address: Optional[str] = None; is_enabled: Optional[bool] = None
    min_confirmations: Optional[str] = None; contract_address: Optional[str] = None

@router.get("/crypto", summary="List crypto networks")
async def list_crypto(db: AsyncSession = Depends(get_db)):
    networks = (await db.execute(select(CryptoNetwork).order_by(CryptoNetwork.name))).scalars().all()
    data = [{"id":n.id,"name":n.name,"symbol":n.symbol,"slug":n.slug,"admin_wallet_address":n.admin_wallet_address,"is_enabled":n.is_enabled,"min_confirmations":n.min_confirmations,"contract_address":n.contract_address} for n in networks]
    return APIResponse(success=True, data=data)

@router.put("/crypto/{network_id}", summary="Update crypto network")
async def update_crypto(network_id: str, data: UpdateCryptoRequest, db: AsyncSession = Depends(get_db)):
    n = (await db.execute(select(CryptoNetwork).where(CryptoNetwork.id == network_id))).scalar_one_or_none()
    if not n: return APIResponse(success=False, message="Not found")
    for k, v in data.model_dump(exclude_none=True).items(): setattr(n, k, v)
    await db.commit()
    return APIResponse(success=True, message=f"{n.name} updated")
