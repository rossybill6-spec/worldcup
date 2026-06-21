from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.core.email import send_email
router = APIRouter()
@router.post("/transactions/email", summary="Email transaction history")
async def email_export(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await send_email(to_email=user.email, subject="Your Transaction History", body="Your transaction history is attached.")
    return APIResponse(success=True, message="Export emailed")
