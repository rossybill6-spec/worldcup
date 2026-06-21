from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.bill_repository import BillRepository
from app.repositories.account_repository import AccountRepository
from app.models.bill_payee import BillPayee
from app.models.bill_payment import BillPayment
from app.models.bill_schedule import BillSchedule
from app.utils.reference_generator import generate_reference

class BillService:
    def __init__(self, db: AsyncSession):
        self.db = db; self.repo = BillRepository(db); self.acct_repo = AccountRepository(db)
    
    async def add_payee(self, user_id: str, data: dict) -> Dict:
        p = BillPayee(user_id=user_id, **data)
        await self.repo.create_payee(p)
        return {"success":True,"payee_id":p.id,"name":p.name}
    
    async def get_payees(self, user_id: str) -> List[Dict]:
        payees = await self.repo.get_payees(user_id)
        return [{"id":p.id,"name":p.name,"account_number":p.account_number,"category":p.category,"nickname":p.nickname} for p in payees]
    
    async def update_payee(self, user_id: str, payee_id: str, data: dict) -> bool:
        p = await self.repo.get_payee(payee_id, user_id)
        if not p: return False
        for k,v in data.items():
            if v is not None: setattr(p, k, v)
        return True
    
    async def delete_payee(self, user_id: str, payee_id: str) -> bool:
        return await self.repo.delete_payee(payee_id, user_id)
    
    async def make_payment(self, user_id: str, data: dict) -> Dict:
        from_acct = await self.acct_repo.find_by_id(data["account_id"])
        if not from_acct or from_acct.user_id != user_id: return {"success":False,"message":"Account not found"}
        if from_acct.available_balance < data["amount"]: return {"success":False,"message":"Insufficient funds"}
        reference = generate_reference("BIL")
        pmt = BillPayment(user_id=user_id, account_id=data["account_id"], payee_id=data.get("payee_id"),
                         amount=data["amount"], fee=0.0, status="pending", reference=reference,
                         scheduled_date=data.get("scheduled_date"), is_recurring=data.get("is_recurring",False),
                         frequency=data.get("frequency"), memo=data.get("memo"))
        await self.repo.create_payment(pmt)
        if data.get("is_recurring") and data.get("frequency"):
            schedule = BillSchedule(user_id=user_id, payee_id=data.get("payee_id"), account_id=data["account_id"],
                                   amount=data["amount"], frequency=data["frequency"],
                                   next_payment_date=data.get("scheduled_date"), memo=data.get("memo"))
            await self.repo.create_schedule(schedule)
        return {"success":True,"reference":reference,"payment_id":pmt.id,"amount":data["amount"],"status":"pending"}
    
    async def get_payments(self, user_id: str, page: int = 1, per_page: int = 20) -> Dict:
        offset = (page-1)*per_page
        payments = await self.repo.get_payments(user_id, per_page, offset)
        items = [{"id":p.id,"amount":p.amount,"fee":p.fee,"status":p.status,"reference":p.reference,"scheduled_date":p.scheduled_date,"is_recurring":p.is_recurring,"memo":p.memo,"created_at":p.created_at.isoformat() if p.created_at else None} for p in payments]
        return {"items":items,"page":page,"per_page":per_page,"total":len(items)}
    
    async def get_schedules(self, user_id: str) -> List[Dict]:
        schedules = await self.repo.get_schedules(user_id)
        return [{"id":s.id,"amount":s.amount,"frequency":s.frequency,"next_payment_date":s.next_payment_date,"is_active":s.is_active,"memo":s.memo} for s in schedules]
    
    async def cancel_schedule(self, user_id: str, schedule_id: str) -> bool:
        return await self.repo.delete_schedule(schedule_id, user_id)
