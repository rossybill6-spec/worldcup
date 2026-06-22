import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.core.config import settings
from app.models.admin import Admin
from app.models.admin_role import AdminRole
from app.utils.hashers import hash_user_password

async def main():
    engine = create_async_engine(settings.DATABASE_URL_ASYNC)
    s = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with s() as db:
        role = (await db.execute(select(AdminRole).where(AdminRole.name == "Super Admin"))).scalar_one_or_none()
        if not role:
            role = AdminRole(name="Super Admin", description="Full access", level="1", is_system="true")
            db.add(role); await db.flush()
        admin = (await db.execute(select(Admin).where(Admin.email == settings.SUPER_ADMIN_EMAIL))).scalar_one_or_none()
        if not admin:
            admin = Admin(email=settings.SUPER_ADMIN_EMAIL, username="superadmin", full_name="Super Admin", password_hash=hash_user_password(settings.SUPER_ADMIN_PASSWORD), role_id=role.id, is_super_admin=True)
            db.add(admin); await db.commit()
            print(f"Super admin created: {settings.SUPER_ADMIN_EMAIL}")
        else:
            print("Super admin already exists")

asyncio.run(main())
