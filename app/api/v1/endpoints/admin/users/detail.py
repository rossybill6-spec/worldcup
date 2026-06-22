from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.schemas.common import APIResponse
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_document import UserDocument
from app.models.user_session import UserSession
from app.models.user_device import UserDevice
from app.models.user_login_history import UserLoginHistory
from app.models.user_activity_log import UserActivityLog
from app.models.user_beneficiary import UserBeneficiary
from app.models.user_linked_account import UserLinkedAccount
from app.models.user_note import UserNote
from app.models.user_tag import UserTag
from app.models.account import Account
from app.models.card import Card
from app.models.deposit import Deposit
from app.models.withdrawal import Withdrawal
router = APIRouter()

@router.get("/{user_id}", summary="Get full user detail")
async def user_detail(user_id: str, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u: return APIResponse(success=False, message="User not found")
    p = (await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))).scalar_one_or_none()
    docs = (await db.execute(select(UserDocument).where(UserDocument.user_id == user_id, UserDocument.is_deleted == False))).scalars().all()
    accounts = (await db.execute(select(Account).where(Account.user_id == user_id, Account.is_deleted == False))).scalars().all()
    cards = (await db.execute(select(Card).where(Card.user_id == user_id, Card.is_deleted == False))).scalars().all()
    sessions = (await db.execute(select(UserSession).where(UserSession.user_id == user_id, UserSession.is_active == True))).scalars().all()
    devices = (await db.execute(select(UserDevice).where(UserDevice.user_id == user_id, UserDevice.is_trusted == True))).scalars().all()
    notes = (await db.execute(select(UserNote).where(UserNote.user_id == user_id, UserNote.is_deleted == False))).scalars().all()
    tags = (await db.execute(select(UserTag).where(UserTag.user_id == user_id, UserTag.is_deleted == False))).scalars().all()
    activity = (await db.execute(select(UserActivityLog).where(UserActivityLog.user_id == user_id).order_by(UserActivityLog.created_at.desc()).limit(20))).scalars().all()
    login_history = (await db.execute(select(UserLoginHistory).where(UserLoginHistory.user_id == user_id).order_by(UserLoginHistory.attempted_at.desc()).limit(10))).scalars().all()
    beneficiaries = (await db.execute(select(UserBeneficiary).where(UserBeneficiary.user_id == user_id, UserBeneficiary.is_deleted == False))).scalars().all()
    linked = (await db.execute(select(UserLinkedAccount).where(UserLinkedAccount.user_id == user_id, UserLinkedAccount.is_deleted == False))).scalars().all()
    deposits = (await db.execute(select(Deposit).where(Deposit.user_id == user_id).order_by(Deposit.created_at.desc()).limit(10))).scalars().all()
    withdrawals = (await db.execute(select(Withdrawal).where(Withdrawal.user_id == user_id).order_by(Withdrawal.created_at.desc()).limit(10))).scalars().all()
    return APIResponse(success=True, data={
        "profile": {"id": u.id, "email": u.email, "username": u.username, "phone": u.phone, "is_active": u.is_active, "is_suspended": u.is_suspended, "is_email_verified": u.is_email_verified, "is_phone_verified": u.is_phone_verified, "is_2fa_enabled": u.is_2fa_enabled, "biometric_enabled": u.biometric_enabled, "kyc_status": u.kyc_status, "failed_login_attempts": u.failed_login_attempts, "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None, "created_at": u.created_at.isoformat() if u.created_at else None},
        "personal": {"first_name": p.first_name if p else None, "last_name": p.last_name if p else None, "date_of_birth": p.date_of_birth.isoformat() if p and p.date_of_birth else None, "ssn_last_four": p.ssn_last_four if p else None, "address": f"{p.address_line1}, {p.city}, {p.state} {p.zip_code}" if p else None},
        "accounts": [{"id": a.id, "account_number": a.account_number, "account_type": a.account_type, "balance": a.balance, "available_balance": a.available_balance, "is_frozen": a.is_frozen} for a in accounts],
        "cards": [{"id": c.id, "last_four": c.last_four, "card_type": c.card_type, "status": c.status, "is_frozen": c.is_frozen} for c in cards],
        "kyc_documents": [{"id": d.id, "type": d.document_type, "status": d.verification_status, "file_url": d.file_url} for d in docs],
        "sessions": [{"id": s.id, "ip": s.ip_address, "device": s.device_name, "created": s.created_at.isoformat() if s.created_at else None} for s in sessions],
        "devices": [{"id": d.id, "name": d.device_name, "last_used": d.last_used_at.isoformat() if d.last_used_at else None} for d in devices],
        "notes": [{"id": n.id, "note": n.note, "author": n.author_name, "pinned": n.is_pinned, "created": n.created_at.isoformat() if n.created_at else None} for n in notes],
        "tags": [t.tag for t in tags],
        "activity": [{"action": a.action, "description": a.description, "ip": a.ip_address, "time": a.created_at.isoformat() if a.created_at else None} for a in activity],
        "login_history": [{"method": h.login_method, "success": h.is_successful, "ip": h.ip_address, "time": h.attempted_at.isoformat() if h.attempted_at else None} for h in login_history],
        "beneficiaries": [{"id": b.id, "name": b.name, "account": b.account_number} for b in beneficiaries],
        "linked_accounts": [{"id": l.id, "bank": l.bank_name, "verified": l.is_verified} for l in linked],
        "recent_deposits": [{"id": d.id, "amount": d.amount, "method": d.method, "status": d.status, "ref": d.reference} for d in deposits],
        "recent_withdrawals": [{"id": w.id, "amount": w.amount, "method": w.method, "status": w.status, "ref": w.reference} for w in withdrawals],
    })
