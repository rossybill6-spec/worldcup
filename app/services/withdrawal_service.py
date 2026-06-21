from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.withdrawal_repository import WithdrawalRepository
from app.repositories.account_repository import AccountRepository
from app.models.withdrawal import Withdrawal
from app.utils.reference_generator import generate_reference

class WithdrawalService:
    def __init__(self, db: AsyncSession):
        self.db = db; self.repo = WithdrawalRepository(db); self.acct_repo = AccountRepository(db)
    
    async def get_methods(self) -> List[Dict]:
        methods = await self.repo.get_methods()
        return [{"id":m.id,"name":m.name,"slug":m.slug,"description":m.description,"is_enabled":m.is_enabled,"min_amount":m.min_amount,"max_amount":m.max_amount,"fee_type":m.fee_type,"fee_amount":m.fee_amount,"processing_time":m.processing_time,"icon":m.icon} for m in methods]
    
    async def create_withdrawal(self, user_id: str, account_id: str, method: str, amount: float, fee: float, extra_data: dict = None) -> Dict:
        account = await self.acct_repo.find_by_id(account_id)
        if not account or account.user_id != user_id: return {"success":False,"message":"Account not found"}
        if account.available_balance < amount: return {"success":False,"message":"Insufficient funds"}
        reference = generate_reference("WTH")
        w = Withdrawal(user_id=user_id, account_id=account_id, method=method, amount=amount, fee=fee, net_amount=amount-fee, currency="USD", status="pending", reference=reference, method_data=str(extra_data) if extra_data else None)
        await self.repo.create_withdrawal(w)
        return {"success":True,"reference":reference,"withdrawal_id":w.id,"amount":amount,"fee":fee,"net_amount":amount-fee,"status":"pending"}
    
    async def get_history(self, user_id: str, page: int = 1, per_page: int = 20) -> Dict:
        offset = (page-1)*per_page
        withdrawals = await self.repo.get_withdrawals_by_user(user_id, per_page, offset)
        items = [{"id":w.id,"method":w.method,"amount":w.amount,"fee":w.fee,"net_amount":w.net_amount,"status":w.status,"reference":w.reference,"currency":w.currency,"created_at":w.created_at.isoformat() if w.created_at else None} for w in withdrawals]
        return {"items":items,"page":page,"per_page":per_page,"total":len(items)}
