"""Deposit service - Handles all deposit methods."""
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.deposit_repository import DepositRepository
from app.repositories.crypto_repository import CryptoRepository
from app.repositories.account_repository import AccountRepository
from app.models.deposit import Deposit
from app.models.deposit_session import DepositSession
from app.utils.reference_generator import generate_reference
from app.utils.qr_code import generate_crypto_qr
from app.utils.deep_link import get_wallet_deep_link
from app.core.config import settings

class DepositService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DepositRepository(db)
        self.crypto_repo = CryptoRepository(db)
        self.account_repo = AccountRepository(db)
    
    async def get_methods(self) -> List[Dict]:
        methods = await self.repo.get_methods()
        return [{"id": m.id, "name": m.name, "slug": m.slug, "description": m.description,
                 "is_enabled": m.is_enabled, "min_amount": m.min_amount, "max_amount": m.max_amount,
                 "fee_type": m.fee_type, "fee_amount": m.fee_amount, "processing_time": m.processing_time,
                 "instructions": m.instructions, "icon": m.icon} for m in methods]
    
    async def initiate_crypto_deposit(self, user_id: str, account_id: str, amount: float, network_slug: str) -> Dict:
        network = await self.crypto_repo.get_network_by_slug(network_slug)
        if not network: return {"success": False, "message": "Network not found"}
        
        reference = generate_reference("DEP")
        deposit = Deposit(user_id=user_id, account_id=account_id, method=f"crypto_{network_slug}",
                         amount=amount, fee=0.0, net_amount=amount, currency="USD",
                         status="pending", reference=reference)
        await self.repo.create_deposit(deposit)
        
        expires = datetime.utcnow() + timedelta(hours=24)
        session = DepositSession(user_id=user_id, deposit_id=deposit.id, network=network_slug,
                                currency=network.symbol, expected_amount=amount,
                                admin_address=network.admin_wallet_address,
                                reference=reference, expires_at=expires)
        await self.repo.create_session(session)
        
        qr_data = f"{network.symbol}:{network.admin_wallet_address}?amount={amount}"
        qr_code = generate_crypto_qr(network.admin_wallet_address, network_slug, amount)
        deep_link_data = get_wallet_deep_link(network_slug, network.admin_wallet_address, amount)
        
        return {"success": True, "session_id": session.id, "reference": reference,
                "address": network.admin_wallet_address, "network": network_slug,
                "expected_amount": amount, "qr_code": f"data:image/png;base64,{qr_code}",
                "deep_link": deep_link_data["deep_link"], "expires_at": expires.isoformat()}
    
    async def create_mock_deposit(self, user_id: str, account_id: str, method: str, amount: float, extra_data: dict = None) -> Dict:
        reference = generate_reference("DEP")
        fee = 0.0
        deposit = Deposit(user_id=user_id, account_id=account_id, method=method,
                         amount=amount, fee=fee, net_amount=amount - fee, currency="USD",
                         status="pending", reference=reference,
                         method_data=str(extra_data) if extra_data else None)
        await self.repo.create_deposit(deposit)
        return {"success": True, "reference": reference, "deposit_id": deposit.id,
                "amount": amount, "fee": fee, "net_amount": amount - fee, "status": "pending"}
    
    async def get_deposit_history(self, user_id: str, page: int = 1, per_page: int = 20) -> Dict:
        offset = (page - 1) * per_page
        deposits = await self.repo.get_deposits_by_user(user_id, per_page, offset)
        items = [{"id": d.id, "method": d.method, "amount": d.amount, "fee": d.fee,
                  "net_amount": d.net_amount, "status": d.status, "reference": d.reference,
                  "currency": d.currency, "created_at": d.created_at.isoformat() if d.created_at else None,
                  "admin_notes": d.admin_notes} for d in deposits]
        return {"items": items, "page": page, "per_page": per_page, "total": len(items)}
