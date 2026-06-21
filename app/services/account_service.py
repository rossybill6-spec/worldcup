"""
Account service - Account creation and balance management.
"""

from typing import Optional, List, Dict
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account_repository import AccountRepository
from app.models.account import Account
from app.utils.generators import generate_account_number


class AccountService:
    """Handles account creation and balance operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AccountRepository(db)
    
    async def create_checking_account(self, user_id: str) -> Account:
        """Create a checking account for a new user."""
        account = Account(
            user_id=user_id,
            account_number=generate_account_number(),
            account_type="checking",
            account_name="Primary Checking",
            balance=0.0,
            available_balance=0.0,
        )
        return await self.repo.create_account(account)
    
    async def create_savings_account(self, user_id: str, account_name: Optional[str] = None, initial_deposit: float = 0.0) -> Account:
        """Create a savings account."""
        # Transfer initial deposit from checking if needed
        if initial_deposit > 0:
            checking = await self.repo.get_checking_account(user_id)
            if checking and checking.available_balance >= initial_deposit:
                await self.repo.update_balance(checking.id, initial_deposit, is_credit=False)
        
        account = Account(
            user_id=user_id,
            account_number=generate_account_number(),
            account_type="savings",
            account_name=account_name or "Savings Account",
            balance=initial_deposit,
            available_balance=initial_deposit,
            interest_rate=0.50,
        )
        return await self.repo.create_account(account)
    
    async def get_user_accounts(self, user_id: str) -> Dict:
        """Get all accounts with total balance."""
        accounts = await self.repo.get_user_accounts(user_id)
        total = sum(a.balance for a in accounts)
        
        return {
            "accounts": [
                {
                    "id": a.id,
                    "account_number": a.account_number,
                    "account_type": a.account_type,
                    "account_name": a.account_name,
                    "balance": a.balance,
                    "available_balance": a.available_balance,
                    "pending_balance": a.pending_balance,
                    "currency": a.currency,
                    "is_active": a.is_active,
                    "is_frozen": a.is_frozen,
                    "interest_rate": a.interest_rate,
                    "overdraft_protection": a.overdraft_protection,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                }
                for a in accounts
            ],
            "total_balance": total,
        }
    
    async def get_account_detail(self, account_id: str, user_id: str) -> Optional[Dict]:
        """Get single account detail."""
        account = await self.repo.find_by_id(account_id)
        if not account or account.user_id != user_id:
            return None
        
        return {
            "id": account.id,
            "account_number": account.account_number,
            "account_type": account.account_type,
            "account_name": account.account_name,
            "balance": account.balance,
            "available_balance": account.available_balance,
            "pending_balance": account.pending_balance,
            "currency": account.currency,
            "is_active": account.is_active,
            "is_frozen": account.is_frozen,
            "interest_rate": account.interest_rate,
            "overdraft_protection": account.overdraft_protection,
            "created_at": account.created_at.isoformat() if account.created_at else None,
        }
