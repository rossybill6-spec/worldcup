"""
Account repository - Database operations for accounts.
"""

from typing import Optional, List
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.models.account_balance import AccountBalance
from app.models.account_statement import AccountStatement


class AccountRepository:
    """Repository for account operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def find_by_id(self, account_id: str) -> Optional[Account]:
        """Find account by ID."""
        result = await self.db.execute(
            select(Account).where(Account.id == account_id, Account.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def find_by_account_number(self, account_number: str) -> Optional[Account]:
        """Find account by account number."""
        result = await self.db.execute(
            select(Account).where(Account.account_number == account_number, Account.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_user_accounts(self, user_id: str) -> List[Account]:
        """Get all accounts for a user."""
        result = await self.db.execute(
            select(Account).where(
                Account.user_id == user_id,
                Account.is_deleted == False,
            ).order_by(Account.created_at)
        )
        return list(result.scalars().all())
    
    async def get_checking_account(self, user_id: str) -> Optional[Account]:
        """Get user's checking account."""
        result = await self.db.execute(
            select(Account).where(
                Account.user_id == user_id,
                Account.account_type == "checking",
                Account.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()
    
    async def create_account(self, account: Account) -> Account:
        """Create a new account."""
        self.db.add(account)
        await self.db.flush()
        return account
    
    async def update_balance(self, account_id: str, amount: float, is_credit: bool = True) -> None:
        """Update account balance."""
        account = await self.find_by_id(account_id)
        if account:
            if is_credit:
                account.balance += amount
                account.available_balance += amount
            else:
                account.balance -= amount
                account.available_balance -= amount
    
    async def get_statements(self, account_id: str) -> List[AccountStatement]:
        """Get statements for an account."""
        result = await self.db.execute(
            select(AccountStatement).where(
                AccountStatement.account_id == account_id,
            ).order_by(AccountStatement.statement_date.desc())
        )
        return list(result.scalars().all())
    
    async def create_statement(self, statement: AccountStatement) -> AccountStatement:
        """Create a statement record."""
        self.db.add(statement)
        await self.db.flush()
        return statement
