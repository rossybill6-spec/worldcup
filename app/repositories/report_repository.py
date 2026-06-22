from typing import List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import Report
from app.models.report_schedule import ReportSchedule

class ReportRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def create(self, r: Report) -> Report: self.db.add(r); await self.db.flush(); return r
    async def get_all(self) -> List[Report]:
        r = await self.db.execute(select(Report).order_by(Report.created_at.desc()).limit(50))
        return list(r.scalars().all())
    async def create_schedule(self, s: ReportSchedule) -> ReportSchedule: self.db.add(s); await self.db.flush(); return s
    async def get_schedules(self) -> List[ReportSchedule]:
        r = await self.db.execute(select(ReportSchedule).where(ReportSchedule.is_active == True))
        return list(r.scalars().all())
