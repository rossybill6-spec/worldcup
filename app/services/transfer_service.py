from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transfer_repository import TransferRepository
from app.repositories.account_repository import AccountRepository
from app.models.transfer import Transfer
from app.models.transfer_template import TransferTemplate
from app.utils.reference_generator import generate_reference

class TransferService:
    def __init__(self, db: AsyncSession):
        self.db = db; self.repo = TransferRepository(db); self.acct_repo = AccountRepository(db)
    
    async def internal_transfer(self, user_id: str, from_id: str, to_id: str, amount: float, memo: str = None) -> Dict:
        from_acct = await self.acct_repo.find_by_id(from_id)
        to_acct = await self.acct_repo.find_by_id(to_id)
        if not from_acct or from_acct.user_id != user_id: return {"success":False,"message":"Source account not found"}
        if not to_acct or to_acct.user_id != user_id: return {"success":False,"message":"Destination account not found"}
        if from_acct.available_balance < amount: return {"success":False,"message":"Insufficient funds"}
        reference = generate_reference("TRF")
        t = Transfer(user_id=user_id, from_account_id=from_id, to_account_id=to_id, transfer_type="internal",
                    amount=amount, fee=0.0, net_amount=amount, currency="USD", status="completed", reference=reference, memo=memo)
        await self.repo.create_transfer(t)
        from_acct.balance -= amount; from_acct.available_balance -= amount
        to_acct.balance += amount; to_acct.available_balance += amount
        return {"success":True,"reference":reference,"transfer_id":t.id,"amount":amount,"fee":0.0,"status":"completed"}
    
    async def external_transfer(self, user_id: str, from_id: str, amount: float, recipient_name: str, recipient_account: str, recipient_routing: str, recipient_bank: str = None, memo: str = None) -> Dict:
        from_acct = await self.acct_repo.find_by_id(from_id)
        if not from_acct or from_acct.user_id != user_id: return {"success":False,"message":"Account not found"}
        if from_acct.available_balance < amount: return {"success":False,"message":"Insufficient funds"}
        reference = generate_reference("TRF")
        t = Transfer(user_id=user_id, from_account_id=from_id, transfer_type="external", amount=amount, fee=0.0,
                    net_amount=amount, currency="USD", status="pending", reference=reference,
                    recipient_name=recipient_name, recipient_account=recipient_account,
                    recipient_routing=recipient_routing, recipient_bank=recipient_bank, memo=memo)
        await self.repo.create_transfer(t)
        from_acct.available_balance -= amount
        return {"success":True,"reference":reference,"transfer_id":t.id,"amount":amount,"fee":0.0,"status":"pending"}
    
    async def wire_transfer(self, user_id: str, from_id: str, amount: float, recipient_name: str, recipient_account: str, recipient_routing: str, recipient_bank: str, swift: str = None, recipient_address: str = None, memo: str = None) -> Dict:
        from_acct = await self.acct_repo.find_by_id(from_id)
        if not from_acct or from_acct.user_id != user_id: return {"success":False,"message":"Account not found"}
        fee = 25.0
        if from_acct.available_balance < (amount + fee): return {"success":False,"message":"Insufficient funds"}
        reference = generate_reference("WIR")
        t = Transfer(user_id=user_id, from_account_id=from_id, transfer_type="wire", amount=amount, fee=fee,
                    net_amount=amount-fee, currency="USD", status="pending", reference=reference,
                    recipient_name=recipient_name, recipient_account=recipient_account,
                    recipient_routing=recipient_routing, recipient_bank=recipient_bank,
                    swift_code=swift, memo=memo)
        await self.repo.create_transfer(t)
        from_acct.available_balance -= (amount + fee)
        return {"success":True,"reference":reference,"transfer_id":t.id,"amount":amount,"fee":fee,"net_amount":amount-fee,"status":"pending"}
    
    async def international_transfer(self, user_id: str, from_id: str, amount: float, recipient_name: str, recipient_account: str, recipient_bank: str, swift: str, country: str, currency: str = "USD", memo: str = None) -> Dict:
        from_acct = await self.acct_repo.find_by_id(from_id)
        if not from_acct or from_acct.user_id != user_id: return {"success":False,"message":"Account not found"}
        fee = 35.0; rate = 0.92 if currency == "EUR" else 1.0; converted = round(amount * rate, 2)
        if from_acct.available_balance < (amount + fee): return {"success":False,"message":"Insufficient funds"}
        reference = generate_reference("INT")
        t = Transfer(user_id=user_id, from_account_id=from_id, transfer_type="international", amount=amount, fee=fee,
                    net_amount=amount-fee, currency=currency, exchange_rate=rate, converted_amount=converted,
                    status="pending", reference=reference, recipient_name=recipient_name,
                    recipient_account=recipient_account, recipient_bank=recipient_bank, swift_code=swift, memo=memo)
        await self.repo.create_transfer(t)
        from_acct.available_balance -= (amount + fee)
        return {"success":True,"reference":reference,"transfer_id":t.id,"amount":amount,"fee":fee,"net_amount":amount-fee,"exchange_rate":rate,"converted_amount":converted,"status":"pending"}
    
    async def get_history(self, user_id: str, page: int = 1, per_page: int = 20) -> Dict:
        offset = (page-1)*per_page
        transfers = await self.repo.get_transfers_by_user(user_id, per_page, offset)
        items = [{"id":t.id,"transfer_type":t.transfer_type,"amount":t.amount,"fee":t.fee,"net_amount":t.net_amount,"status":t.status,"reference":t.reference,"currency":t.currency,"recipient_name":t.recipient_name,"memo":t.memo,"created_at":t.created_at.isoformat() if t.created_at else None} for t in transfers]
        return {"items":items,"page":page,"per_page":per_page,"total":len(items)}
    
    async def create_template(self, user_id: str, data: dict) -> Dict:
        t = TransferTemplate(user_id=user_id, **data)
        await self.repo.create_template(t)
        return {"success":True,"template_id":t.id,"name":t.name}
    
    async def get_templates(self, user_id: str) -> List[Dict]:
        templates = await self.repo.get_templates_by_user(user_id)
        return [{"id":t.id,"name":t.name,"transfer_type":t.transfer_type,"amount":t.amount,"frequency":t.frequency,"is_active":t.is_active} for t in templates]
    
    async def delete_template(self, user_id: str, template_id: str) -> bool:
        return await self.repo.delete_template(template_id, user_id)
