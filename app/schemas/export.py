from pydantic import BaseModel
from typing import Optional

class ExportRequest(BaseModel):
    format: str = "csv"; transaction_type: Optional[str] = None
    status: Optional[str] = None; start_date: Optional[str] = None
    end_date: Optional[str] = None; account_id: Optional[str] = None
