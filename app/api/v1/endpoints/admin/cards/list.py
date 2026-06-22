from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.card import Card
router = APIRouter()
@router.get("/all", summary="List all cards in system")
async def list_all_cards(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)):
    q = select(Card).where(Card.is_deleted == False).order_by(Card.created_at.desc())
    total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar()
    rows = (await db.execute(q.offset((page-1)*per_page).limit(per_page))).scalars().all()
    items = [{"id":c.id,"user_id":c.user_id,"card_type":c.card_type,"last_four":c.last_four,"status":c.status,"is_frozen":c.is_frozen,"created_at":c.created_at.isoformat() if c.created_at else None} for c in rows]
    return APIResponse(success=True, data={"items":items,"total":total,"page":page})
