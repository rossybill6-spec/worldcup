"""Crypto repository."""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.crypto_network import CryptoNetwork

class CryptoRepository:
    def __init__(self, db: AsyncSession): self.db = db
    
    async def get_networks(self) -> List[CryptoNetwork]:
        r = await self.db.execute(select(CryptoNetwork).where(CryptoNetwork.is_enabled == True))
        return list(r.scalars().all())
    
    async def get_network_by_slug(self, slug: str) -> Optional[CryptoNetwork]:
        r = await self.db.execute(select(CryptoNetwork).where(CryptoNetwork.slug == slug))
        return r.scalar_one_or_none()
