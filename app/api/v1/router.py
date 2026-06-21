from fastapi import APIRouter
from app.api.v1.endpoints.auth.signup import router as signup_router
from app.api.v1.endpoints.auth.login import router as login_router
from app.api.v1.endpoints.auth.logout import router as logout_router
from app.api.v1.endpoints.auth.verify_email import router as verify_email_router
from app.api.v1.endpoints.auth.verify_phone import router as verify_phone_router
from app.api.v1.endpoints.auth.forgot_password import router as forgot_password_router
from app.api.v1.endpoints.auth.reset_password import router as reset_password_router
from app.api.v1.endpoints.auth.forgot_username import router as forgot_username_router
from app.api.v1.endpoints.auth.refresh_token import router as refresh_token_router
from app.api.v1.endpoints.auth.verify_2fa import router as verify_2fa_router
from app.api.v1.endpoints.auth.setup_2fa import router as setup_2fa_router
from app.api.v1.endpoints.auth.biometric import router as biometric_router
from app.api.v1.endpoints.users.profile import router as profile_router
from app.api.v1.endpoints.users.security import router as security_router
from app.api.v1.endpoints.users.documents import router as documents_router
from app.api.v1.endpoints.users.kyc import router as kyc_router
from app.api.v1.endpoints.users.beneficiaries import router as beneficiaries_router
from app.api.v1.endpoints.users.linked_accounts import router as linked_accounts_router
from app.api.v1.endpoints.users.limits import router as limits_router
from app.api.v1.endpoints.users.notifications import router as notification_prefs_router
from app.api.v1.endpoints.users.preferences import router as preferences_router
from app.api.v1.endpoints.users.devices import router as devices_router
from app.api.v1.endpoints.users.sessions import router as sessions_router
from app.api.v1.endpoints.users.activity import router as activity_router
from app.api.v1.endpoints.users.close_account import router as close_account_router
from app.api.v1.endpoints.accounts.checking import router as checking_router
from app.api.v1.endpoints.accounts.savings import router as savings_router
from app.api.v1.endpoints.accounts.balance import router as balance_router
from app.api.v1.endpoints.accounts.statements import router as statements_router
from app.api.v1.endpoints.deposits.methods import router as deposit_methods_router
from app.api.v1.endpoints.deposits.crypto import router as crypto_deposit_router
from app.api.v1.endpoints.deposits.ach import router as ach_deposit_router
from app.api.v1.endpoints.deposits.wire import router as wire_deposit_router
from app.api.v1.endpoints.deposits.check import router as check_deposit_router
from app.api.v1.endpoints.deposits.cash import router as cash_deposit_router
from app.api.v1.endpoints.deposits.direct_deposit import router as dd_deposit_router
from app.api.v1.endpoints.deposits.p2p import router as p2p_deposit_router
from app.api.v1.endpoints.deposits.history import router as deposit_history_router

api_router = APIRouter()
api_router.include_router(signup_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(login_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(logout_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(verify_email_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(verify_phone_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(forgot_password_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(reset_password_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(forgot_username_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(refresh_token_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(verify_2fa_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(setup_2fa_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(biometric_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(profile_router, prefix="/users", tags=["User Profile"])
api_router.include_router(security_router, prefix="/users", tags=["User Security"])
api_router.include_router(documents_router, prefix="/users", tags=["KYC Documents"])
api_router.include_router(kyc_router, prefix="/users", tags=["KYC Status"])
api_router.include_router(beneficiaries_router, prefix="/users", tags=["Beneficiaries"])
api_router.include_router(linked_accounts_router, prefix="/users", tags=["Linked Accounts"])
api_router.include_router(limits_router, prefix="/users", tags=["Limits"])
api_router.include_router(notification_prefs_router, prefix="/users", tags=["Notification Preferences"])
api_router.include_router(preferences_router, prefix="/users", tags=["App Preferences"])
api_router.include_router(devices_router, prefix="/users", tags=["Devices"])
api_router.include_router(sessions_router, prefix="/users", tags=["Sessions"])
api_router.include_router(activity_router, prefix="/users", tags=["Activity"])
api_router.include_router(close_account_router, prefix="/users", tags=["Account"])
api_router.include_router(checking_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(savings_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(balance_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(statements_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(deposit_methods_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(crypto_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(ach_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(wire_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(check_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(cash_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(dd_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(p2p_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(deposit_history_router, prefix="/deposits", tags=["Deposits"])
from app.api.v1.endpoints.withdrawals.methods import router as w_methods_router
from app.api.v1.endpoints.withdrawals.crypto import router as w_crypto_router
from app.api.v1.endpoints.withdrawals.ach import router as w_ach_router
from app.api.v1.endpoints.withdrawals.wire import router as w_wire_router
from app.api.v1.endpoints.withdrawals.card_payout import router as w_card_router
from app.api.v1.endpoints.withdrawals.cash_pickup import router as w_cash_router
from app.api.v1.endpoints.withdrawals.check_mail import router as w_check_router
from app.api.v1.endpoints.withdrawals.internal import router as w_internal_router
from app.api.v1.endpoints.withdrawals.history import router as w_history_router
api_router.include_router(w_methods_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_crypto_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_ach_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_wire_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_card_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_cash_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_check_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_internal_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_history_router, prefix="/withdrawals", tags=["Withdrawals"])
from app.api.v1.endpoints.transfers.internal import router as t_internal_router
from app.api.v1.endpoints.transfers.external import router as t_external_router
from app.api.v1.endpoints.transfers.wire import router as t_wire_router
from app.api.v1.endpoints.transfers.international import router as t_intl_router
from app.api.v1.endpoints.transfers.templates import router as t_templates_router
from app.api.v1.endpoints.transfers.history import router as t_history_router
api_router.include_router(t_internal_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_external_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_wire_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_intl_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_templates_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_history_router, prefix="/transfers", tags=["Transfers"])
from app.api.v1.endpoints.bills.payees import router as bills_payees_router
from app.api.v1.endpoints.bills.payments import router as bills_payments_router
from app.api.v1.endpoints.bills.schedules import router as bills_schedules_router
from app.api.v1.endpoints.bills.history import router as bills_history_router
api_router.include_router(bills_payees_router, prefix="/bills", tags=["Bill Pay"])
api_router.include_router(bills_payments_router, prefix="/bills", tags=["Bill Pay"])
api_router.include_router(bills_schedules_router, prefix="/bills", tags=["Bill Pay"])
api_router.include_router(bills_history_router, prefix="/bills", tags=["Bill Pay"])
from app.api.v1.endpoints.cards.virtual import router as cards_router
from app.api.v1.endpoints.cards.physical import router as cards_physical_router
from app.api.v1.endpoints.cards.limits import router as cards_limits_router
from app.api.v1.endpoints.cards.settings import router as cards_settings_router
from app.api.v1.endpoints.cards.transactions import router as cards_tx_router
from app.api.v1.endpoints.cards.digital_wallet import router as cards_wallet_router
from app.api.v1.endpoints.cards.dispute import router as cards_dispute_router
api_router.include_router(cards_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_physical_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_limits_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_settings_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_tx_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_wallet_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_dispute_router, prefix="/cards", tags=["Cards"])
from app.api.v1.endpoints.dashboard.overview import router as dashboard_router
from app.api.v1.endpoints.dashboard.recent import router as recent_router
from app.api.v1.endpoints.export.csv import router as export_csv_router
from app.api.v1.endpoints.export.pdf import router as export_json_router
from app.api.v1.endpoints.export.email import router as export_email_router
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(recent_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(export_csv_router, prefix="/export", tags=["Export"])
api_router.include_router(export_json_router, prefix="/export", tags=["Export"])
api_router.include_router(export_email_router, prefix="/export", tags=["Export"])
from app.api.v1.endpoints.notifications.list import router as notif_list_router
from app.api.v1.endpoints.notifications.read import router as notif_read_router
from app.api.v1.endpoints.notifications.preferences import router as notif_prefs_router
from app.api.v1.endpoints.alerts.balance import router as alerts_router
api_router.include_router(notif_list_router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(notif_read_router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(notif_prefs_router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
