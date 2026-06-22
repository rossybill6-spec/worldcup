from pydantic import BaseModel, Field
from typing import Optional, List

class GenerateReportRequest(BaseModel):
    report_type: str = Field(..., description="users, transactions, revenue, fees, deposits, withdrawals")
    start_date: Optional[str] = None; end_date: Optional[str] = None
    format: str = "json"

class ScheduleReportRequest(BaseModel):
    report_type: str; frequency: str = Field(..., description="daily, weekly, monthly")
    recipients: str = ""; format: str = "csv"

class ReportResponse(BaseModel):
    id: str; name: str; report_type: str; format: str
    created_at: Optional[str] = None; file_url: Optional[str] = None
    class Config: from_attributes = True
