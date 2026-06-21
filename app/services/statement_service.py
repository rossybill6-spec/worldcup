"""
Statement service - Monthly statement generation.
"""

from typing import Optional, List, Dict
from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account_repository import AccountRepository
from app.models.account_statement import AccountStatement


class StatementService:
    """Handles statement generation and retrieval."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AccountRepository(db)
    
    async def generate_statement(self, account_id: str) -> Optional[AccountStatement]:
        """Generate a statement for the current month."""
        account = await self.repo.find_by_id(account_id)
        if not account:
            return None
        
        today = date.today()
        first_of_month = today.replace(day=1)
        last_month = first_of_month - timedelta(days=1)
        period_start = last_month.replace(day=1)
        
        statement = AccountStatement(
            account_id=account_id,
            statement_date=today,
            period_start=period_start,
            period_end=last_month,
            opening_balance=account.balance,
            closing_balance=account.balance,
            total_deposits=0.0,
            total_withdrawals=0.0,
            total_fees=0.0,
            interest_earned=0.0,
        )
        return await self.repo.create_statement(statement)
    
    async def get_statements(self, account_id: str) -> List[Dict]:
        """Get all statements for an account."""
        statements = await self.repo.get_statements(account_id)
        return [
            {
                "id": s.id,
                "statement_date": s.statement_date.isoformat() if s.statement_date else None,
                "period_start": s.period_start.isoformat() if s.period_start else None,
                "period_end": s.period_end.isoformat() if s.period_end else None,
                "opening_balance": s.opening_balance,
                "closing_balance": s.closing_balance,
                "total_deposits": s.total_deposits,
                "total_withdrawals": s.total_withdrawals,
                "total_fees": s.total_fees,
                "interest_earned": s.interest_earned,
                "file_url": s.file_url,
            }
            for s in statements
        ]
