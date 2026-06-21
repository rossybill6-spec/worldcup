from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services.transaction_service import TransactionService
router = APIRouter()

@router.get("/recent-transactions", summary="Recent transactions")
async def recent(limit: int = Query(10, ge=1, le=50), user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = TransactionService(db); txs = await svc.get_recent(user.id, limit)
    return APIResponse(success=True, message="Recent transactions", data=txs)
