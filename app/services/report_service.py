from typing import Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.report_repository import ReportRepository
from app.repositories.admin_repository import AdminRepository
from app.models.report import Report
from app.models.report_schedule import ReportSchedule

class ReportService:
    def __init__(self, db: AsyncSession): self.db = db; self.repo = ReportRepository(db); self.admin_repo = AdminRepository(db)
    
    async def generate(self, report_type: str, start_date: str = None, end_date: str = None) -> Dict:
        if report_type == "users": return {"type": "users", "total_users": await self.admin_repo.count_users(), "generated_at": datetime.utcnow().isoformat()}
        elif report_type == "transactions":
            from app.models.transaction import Transaction
            from sqlalchemy import select, func
            r = await self.db.execute(select(func.count(), func.sum(Transaction.amount)).select_from(Transaction))
            count, total = r.one()
            return {"type": "transactions", "count": count or 0, "total_volume": float(total or 0), "generated_at": datetime.utcnow().isoformat()}
        elif report_type == "revenue":
            from app.models.transaction import Transaction
            from sqlalchemy import select, func
            r = await self.db.execute(select(func.sum(Transaction.fee)).select_from(Transaction))
            fees = r.scalar() or 0
            return {"type": "revenue", "total_fees": float(fees), "generated_at": datetime.utcnow().isoformat()}
        elif report_type == "deposits":
            from app.models.deposit import Deposit
            from sqlalchemy import select, func
            r = await self.db.execute(select(func.count(), func.sum(Deposit.amount)).select_from(Deposit))
            count, total = r.one()
            return {"type": "deposits", "count": count or 0, "total": float(total or 0), "generated_at": datetime.utcnow().isoformat()}
        elif report_type == "withdrawals":
            from app.models.withdrawal import Withdrawal
            from sqlalchemy import select, func
            r = await self.db.execute(select(func.count(), func.sum(Withdrawal.amount)).select_from(Withdrawal))
            count, total = r.one()
            return {"type": "withdrawals", "count": count or 0, "total": float(total or 0), "generated_at": datetime.utcnow().isoformat()}
        return {"type": report_type, "generated_at": datetime.utcnow().isoformat()}
    
    async def save_report(self, name: str, report_type: str, created_by: str, data: Dict) -> Report:
        r = Report(name=name, report_type=report_type, parameters=data, created_by=created_by)
        return await self.repo.create(r)
    
    async def get_reports(self): return await self.repo.get_all()
    
    async def schedule(self, report_type: str, frequency: str, recipients: str, format: str, created_by: str) -> ReportSchedule:
        s = ReportSchedule(report_type=report_type, frequency=frequency, recipients=recipients, format=format, created_by=created_by)
        return await self.repo.create_schedule(s)
