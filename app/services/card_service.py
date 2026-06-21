from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.card_repository import CardRepository
from app.repositories.account_repository import AccountRepository
from app.models.card import Card
from app.models.card_transaction import CardTransaction
from app.utils.card_generator import generate_card_number, generate_cvv, generate_pin, generate_expiry, mask_card_number
from app.utils.hashers import hash_user_pin, check_user_pin

class CardService:
    def __init__(self, db: AsyncSession): self.db = db; self.repo = CardRepository(db)
    
    async def create_virtual_card(self, user_id: str, account_id: str, cardholder_name: str) -> Dict:
        card_number = generate_card_number()
        month, year = generate_expiry()
        cvv = generate_cvv()
        pin = generate_pin()
        card = Card(user_id=user_id, account_id=account_id, card_number=card_number,
                   card_type="virtual", expiry_month=month, expiry_year=year, cvv=cvv,
                   pin_hash=hash_user_pin(pin), cardholder_name=cardholder_name,
                   last_four=card_number[-4:])
        await self.repo.create_card(card)
        return {"card_id": card.id, "card_number": card_number, "expiry": f"{month}/{year[-2:]}",
                "cvv": cvv, "pin": pin, "last_four": card.last_four,
                "card_number_masked": mask_card_number(card_number)}
    
    async def get_cards(self, user_id: str) -> List[Dict]:
        cards = await self.repo.get_user_cards(user_id)
        return [{"id": c.id, "card_type": c.card_type, "card_number_masked": mask_card_number(c.card_number),
                "expiry_month": c.expiry_month, "expiry_year": c.expiry_year, "cardholder_name": c.cardholder_name,
                "status": c.status, "is_frozen": c.is_frozen, "daily_spending_limit": c.daily_spending_limit,
                "online_purchases": c.online_purchases, "international": c.international,
                "contactless": c.contactless, "apple_pay": c.apple_pay, "google_pay": c.google_pay,
                "samsung_pay": c.samsung_pay, "last_four": c.last_four,
                "created_at": c.created_at.isoformat() if c.created_at else None} for c in cards]
    
    async def get_card_detail(self, card_id: str, user_id: str) -> Optional[Dict]:
        c = await self.repo.get_card(card_id, user_id)
        if not c: return None
        return {"id": c.id, "card_number": c.card_number, "card_number_masked": mask_card_number(c.card_number),
                "expiry_month": c.expiry_month, "expiry_year": c.expiry_year, "cvv": c.cvv,
                "cardholder_name": c.cardholder_name, "status": c.status, "is_frozen": c.is_frozen,
                "daily_spending_limit": c.daily_spending_limit, "per_transaction_limit": c.per_transaction_limit,
                "atm_withdrawal_limit": c.atm_withdrawal_limit, "online_purchases": c.online_purchases,
                "international": c.international, "contactless": c.contactless, "last_four": c.last_four}
    
    async def freeze_card(self, card_id: str, user_id: str) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if c: c.is_frozen = True; return True
        return False
    
    async def unfreeze_card(self, card_id: str, user_id: str) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if c: c.is_frozen = False; return True
        return False
    
    async def update_limits(self, card_id: str, user_id: str, data: dict) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if not c: return False
        for k,v in data.items():
            if v is not None: setattr(c, k, v)
        return True
    
    async def update_settings(self, card_id: str, user_id: str, data: dict) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if not c: return False
        for k,v in data.items():
            if v is not None: setattr(c, k, v)
        return True
    
    async def verify_pin(self, card_id: str, user_id: str, pin: str) -> Optional[str]:
        c = await self.repo.get_card(card_id, user_id)
        if c and check_user_pin(pin, c.pin_hash): return "PIN verified"
        return None
    
    async def request_physical(self, card_id: str, user_id: str) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if c: c.card_type = "physical_requested"; return True
        return False
    
    async def activate_physical(self, card_id: str, user_id: str, last_four: str) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if c and c.last_four == last_four: c.card_type = "physical"; c.status = "active"; return True
        return False
    
    async def setup_digital_wallet(self, card_id: str, user_id: str, wallet_type: str) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if not c: return False
        if wallet_type == "apple_pay": c.apple_pay = True
        elif wallet_type == "google_pay": c.google_pay = True
        elif wallet_type == "samsung_pay": c.samsung_pay = True
        return True
    
    async def get_transactions(self, card_id: str, user_id: str) -> List[Dict]:
        txs = await self.repo.get_transactions(card_id)
        return [{"id": t.id, "amount": t.amount, "merchant": t.merchant, "category": t.category,
                "status": t.status, "transaction_type": t.transaction_type, "reference": t.reference,
                "location": t.location, "created_at": t.created_at.isoformat() if t.created_at else None} for t in txs]
    
    async def file_dispute(self, card_id: str, user_id: str, transaction_id: str, reason: str) -> Dict:
        return {"success": True, "dispute_id": f"DSP-{transaction_id[:8]}", "status": "filed", "reason": reason}
    
    async def report_lost_stolen(self, card_id: str, user_id: str) -> bool:
        c = await self.repo.get_card(card_id, user_id)
        if c: c.is_frozen = True; c.status = "reported_lost"; return True
        return False
