from pydantic import BaseModel
from typing import List, Optional

class DashboardOverview(BaseModel):
    total_balance: float; available_balance: float; pending_balance: float
    accounts: list; recent_transactions: list
    notification_count: int = 0; pending_deposits: int = 0
    pending_withdrawals: int = 0
