"""
Statement endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.services.statement_service import StatementService

router = APIRouter()


@router.get("/{account_id}/statements", response_model=APIResponse, summary="Get account statements")
async def get_statements(
    account_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get monthly statements for an account."""
    repo = AccountRepository(db)
    account = await repo.find_by_id(account_id)
    if not account or account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    service = StatementService(db)
    statements = await service.get_statements(account_id)
    return APIResponse(success=True, message="Statements retrieved", data=statements)


@router.post("/{account_id}/statements/generate", response_model=APIResponse, summary="Generate statement")
async def generate_statement(
    account_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a monthly statement for an account."""
    repo = AccountRepository(db)
    account = await repo.find_by_id(account_id)
    if not account or account.user_id != user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    service = StatementService(db)
    statement = await service.generate_statement(account_id)
    await db.commit()
    
    return APIResponse(
        success=True,
        message="Statement generated",
        data={"id": statement.id, "statement_date": statement.statement_date.isoformat() if statement.statement_date else None},
    )
