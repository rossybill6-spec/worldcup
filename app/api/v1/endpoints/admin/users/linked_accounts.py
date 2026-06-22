from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
router = APIRouter()
@router.get("/{user_id}/linked_accounts", summary="Get user linked_accounts")
async def get_linked_accounts(user_id: str, db: AsyncSession = Depends(get_db)):
    return APIResponse(success=True, message="linked_accounts data", data=[])
