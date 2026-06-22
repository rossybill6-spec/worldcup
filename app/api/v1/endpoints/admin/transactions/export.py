from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import PlainTextResponse
import csv, io
from app.core.database import get_db
from app.models.transaction import Transaction
from sqlalchemy import select
router = APIRouter()
@router.get("/export/csv", summary="Export transactions CSV")
async def export_csv(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Transaction).order_by(Transaction.created_at.desc()).limit(5000))).scalars().all()
    output = io.StringIO()
    w = csv.DictWriter(output, fieldnames=["id","type","amount","fee","net","status","reference","description","user_id","created_at"])
    w.writeheader()
    for t in rows: w.writerow({"id":t.id,"type":t.transaction_type,"amount":t.amount,"fee":t.fee,"net":t.net_amount,"status":t.status,"reference":t.reference,"description":t.description,"user_id":t.user_id,"created_at":t.created_at.isoformat() if t.created_at else ""})
    return PlainTextResponse(output.getvalue(), media_type="text/csv", headers={"Content-Disposition":"attachment; filename=transactions.csv"})
