from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.core.config import settings
from app.models.base import Base
from app.models.user import User; from app.models.user_profile import UserProfile
from app.models.user_session import UserSession; from app.models.user_device import UserDevice
from app.models.user_login_history import UserLoginHistory; from app.models.user_activity_log import UserActivityLog
from app.models.user_security_question import UserSecurityQuestion; from app.models.user_2fa import User2FA
from app.models.user_notification import UserNotification; from app.models.user_notification_preference import UserNotificationPreference
from app.models.user_document import UserDocument; from app.models.user_beneficiary import UserBeneficiary
from app.models.user_linked_account import UserLinkedAccount; from app.models.user_limit import UserLimit
from app.models.user_tag import UserTag; from app.models.user_note import UserNote
from app.models.account import Account; from app.models.account_balance import AccountBalance
from app.models.account_statement import AccountStatement
from app.models.deposit import Deposit; from app.models.deposit_method import DepositMethod
from app.models.deposit_session import DepositSession
from app.models.crypto_network import CryptoNetwork; from app.models.crypto_wallet import CryptoWallet
from app.models.crypto_transaction import CryptoTransaction
from app.models.withdrawal import Withdrawal; from app.models.withdrawal_method import WithdrawalMethod
from app.models.transfer import Transfer; from app.models.transfer_template import TransferTemplate
from app.models.bill_payee import BillPayee; from app.models.bill_payment import BillPayment
from app.models.bill_schedule import BillSchedule
from app.models.card import Card; from app.models.card_transaction import CardTransaction
from app.models.card_limit import CardLimit
from app.models.transaction import Transaction; from app.models.transaction_dispute import TransactionDispute
from app.models.notification import Notification; from app.models.notification_template import NotificationTemplate
from app.models.alert import Alert; from app.models.alert_preference import AlertPreference
from app.models.admin import Admin; from app.models.admin_role import AdminRole
from app.models.admin_permission import AdminPermission; from app.models.admin_session import AdminSession
from app.models.admin_activity_log import AdminActivityLog
from app.models.system_config import SystemConfig
from app.models.fee_schedule import FeeSchedule; from app.models.interest_rate import InterestRate
from app.models.report import Report; from app.models.report_schedule import ReportSchedule
from app.models.audit_log import AuditLog
config = context.config; config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
if config.config_file_name is not None: fileConfig(config.config_file_name)
target_metadata = Base.metadata
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction(): context.run_migrations()
def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction(): context.run_migrations()
if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()
