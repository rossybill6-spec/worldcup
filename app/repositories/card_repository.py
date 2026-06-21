from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.card import Card
from app.models.card_transaction import CardTransaction

class CardRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create_card(self, c: Card) -> Card: self.db.add(c); await self.db.flush(); return c
    async def get_user_cards(self, user_id: str) -> List[Card]:
        r = await self.db.execute(select(Card).where(Card.user_id == user_id, Card.is_deleted == False))
        return list(r.scalars().all())
    async def get_card(self, card_id: str, user_id: str) -> Optional[Card]:
        r = await self.db.execute(select(Card).where(Card.id == card_id, Card.user_id == user_id))
        return r.scalar_one_or_none()
    async def create_transaction(self, t: CardTransaction) -> CardTransaction: self.db.add(t); await self.db.flush(); return t
    async def get_transactions(self, card_id: str, limit: int = 20) -> List[CardTransaction]:
        r = await self.db.execute(select(CardTransaction).where(CardTransaction.card_id == card_id).order_by(CardTransaction.created_at.desc()).limit(limit))
        return list(r.scalars().all())
