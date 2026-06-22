from fastapi import APIRouter

# Auth
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

# Users
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

# Accounts
from app.api.v1.endpoints.accounts.checking import router as checking_router
from app.api.v1.endpoints.accounts.savings import router as savings_router
from app.api.v1.endpoints.accounts.balance import router as balance_router
from app.api.v1.endpoints.accounts.statements import router as statements_router

# Deposits
from app.api.v1.endpoints.deposits.methods import router as deposit_methods_router
from app.api.v1.endpoints.deposits.crypto import router as crypto_deposit_router
from app.api.v1.endpoints.deposits.ach import router as ach_deposit_router
from app.api.v1.endpoints.deposits.wire import router as wire_deposit_router
from app.api.v1.endpoints.deposits.check import router as check_deposit_router
from app.api.v1.endpoints.deposits.cash import router as cash_deposit_router
from app.api.v1.endpoints.deposits.direct_deposit import router as dd_deposit_router
from app.api.v1.endpoints.deposits.p2p import router as p2p_deposit_router
from app.api.v1.endpoints.deposits.history import router as deposit_history_router

# Withdrawals
from app.api.v1.endpoints.withdrawals.methods import router as w_methods_router
from app.api.v1.endpoints.withdrawals.crypto import router as w_crypto_router
from app.api.v1.endpoints.withdrawals.ach import router as w_ach_router
from app.api.v1.endpoints.withdrawals.wire import router as w_wire_router
from app.api.v1.endpoints.withdrawals.card_payout import router as w_card_router
from app.api.v1.endpoints.withdrawals.cash_pickup import router as w_cash_router
from app.api.v1.endpoints.withdrawals.check_mail import router as w_check_router
from app.api.v1.endpoints.withdrawals.internal import router as w_internal_router
from app.api.v1.endpoints.withdrawals.history import router as w_history_router

# Transfers
from app.api.v1.endpoints.transfers.internal import router as t_internal_router
from app.api.v1.endpoints.transfers.external import router as t_external_router
from app.api.v1.endpoints.transfers.wire import router as t_wire_router
from app.api.v1.endpoints.transfers.international import router as t_intl_router
from app.api.v1.endpoints.transfers.templates import router as t_templates_router
from app.api.v1.endpoints.transfers.history import router as t_history_router

# Bills
from app.api.v1.endpoints.bills.payees import router as bills_payees_router
from app.api.v1.endpoints.bills.payments import router as bills_payments_router
from app.api.v1.endpoints.bills.schedules import router as bills_schedules_router
from app.api.v1.endpoints.bills.history import router as bills_history_router

# Cards
from app.api.v1.endpoints.cards.virtual import router as cards_router
from app.api.v1.endpoints.cards.physical import router as cards_physical_router
from app.api.v1.endpoints.cards.limits import router as cards_limits_router
from app.api.v1.endpoints.cards.settings import router as cards_settings_router
from app.api.v1.endpoints.cards.transactions import router as cards_tx_router
from app.api.v1.endpoints.cards.digital_wallet import router as cards_wallet_router
from app.api.v1.endpoints.cards.dispute import router as cards_dispute_router

# Dashboard
from app.api.v1.endpoints.dashboard.overview import router as dashboard_router
from app.api.v1.endpoints.dashboard.recent import router as recent_router

# Export
from app.api.v1.endpoints.export.csv import router as export_csv_router
from app.api.v1.endpoints.export.pdf import router as export_json_router
from app.api.v1.endpoints.export.email import router as export_email_router

# Notifications
from app.api.v1.endpoints.notifications.list import router as notif_list_router
from app.api.v1.endpoints.notifications.read import router as notif_read_router
from app.api.v1.endpoints.notifications.preferences import router as notif_prefs_router

# Alerts
from app.api.v1.endpoints.alerts.balance import router as alerts_router

# Admin
from app.api.v1.endpoints.admin.auth.login import router as admin_login_router
from app.api.v1.endpoints.admin.auth.logout import router as admin_logout_router
from app.api.v1.endpoints.admin.auth.refresh import router as admin_refresh_router
from app.api.v1.endpoints.admin.auth.verify_2fa import router as admin_2fa_router
from app.api.v1.endpoints.admin.dashboard.stats import router as admin_stats_router
from app.api.v1.endpoints.admin.dashboard.health import router as admin_health_router

# Admin Users
from app.api.v1.endpoints.admin.users.list import router as admin_users_list
from app.api.v1.endpoints.admin.users.detail import router as admin_users_detail
from app.api.v1.endpoints.admin.users.edit import router as admin_users_edit
from app.api.v1.endpoints.admin.users.suspend import router as admin_users_suspend
from app.api.v1.endpoints.admin.users.delete import router as admin_users_delete
from app.api.v1.endpoints.admin.users.kyc import router as admin_users_kyc
from app.api.v1.endpoints.admin.users.limits import router as admin_users_limits
from app.api.v1.endpoints.admin.users.notes import router as admin_users_notes
from app.api.v1.endpoints.admin.users.tags import router as admin_users_tags
from app.api.v1.endpoints.admin.users.balance import router as admin_users_balance
from app.api.v1.endpoints.admin.users.accounts import router as admin_users_accounts
from app.api.v1.endpoints.admin.users.cards import router as admin_users_cards
from app.api.v1.endpoints.admin.users.security import router as admin_users_security
from app.api.v1.endpoints.admin.users.sessions import router as admin_users_sessions
from app.api.v1.endpoints.admin.users.bulk import router as admin_users_bulk

api_router = APIRouter()

# Auth
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

# Users
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

# Accounts
api_router.include_router(checking_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(savings_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(balance_router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(statements_router, prefix="/accounts", tags=["Accounts"])

# Deposits
api_router.include_router(deposit_methods_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(crypto_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(ach_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(wire_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(check_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(cash_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(dd_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(p2p_deposit_router, prefix="/deposits", tags=["Deposits"])
api_router.include_router(deposit_history_router, prefix="/deposits", tags=["Deposits"])

# Withdrawals
api_router.include_router(w_methods_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_crypto_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_ach_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_wire_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_card_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_cash_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_check_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_internal_router, prefix="/withdrawals", tags=["Withdrawals"])
api_router.include_router(w_history_router, prefix="/withdrawals", tags=["Withdrawals"])

# Transfers
api_router.include_router(t_internal_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_external_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_wire_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_intl_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_templates_router, prefix="/transfers", tags=["Transfers"])
api_router.include_router(t_history_router, prefix="/transfers", tags=["Transfers"])

# Bills
api_router.include_router(bills_payees_router, prefix="/bills", tags=["Bill Pay"])
api_router.include_router(bills_payments_router, prefix="/bills", tags=["Bill Pay"])
api_router.include_router(bills_schedules_router, prefix="/bills", tags=["Bill Pay"])
api_router.include_router(bills_history_router, prefix="/bills", tags=["Bill Pay"])

# Cards
api_router.include_router(cards_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_physical_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_limits_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_settings_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_tx_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_wallet_router, prefix="/cards", tags=["Cards"])
api_router.include_router(cards_dispute_router, prefix="/cards", tags=["Cards"])

# Dashboard
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(recent_router, prefix="/dashboard", tags=["Dashboard"])

# Export
api_router.include_router(export_csv_router, prefix="/export", tags=["Export"])
api_router.include_router(export_json_router, prefix="/export", tags=["Export"])
api_router.include_router(export_email_router, prefix="/export", tags=["Export"])

# Notifications
api_router.include_router(notif_list_router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(notif_read_router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(notif_prefs_router, prefix="/notifications", tags=["Notifications"])

# Alerts
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])

# Admin Auth
api_router.include_router(admin_login_router, prefix="/admin", tags=["Admin Auth"])
api_router.include_router(admin_logout_router, prefix="/admin", tags=["Admin Auth"])
api_router.include_router(admin_refresh_router, prefix="/admin", tags=["Admin Auth"])
api_router.include_router(admin_2fa_router, prefix="/admin", tags=["Admin Auth"])

# Admin Dashboard
api_router.include_router(admin_stats_router, prefix="/admin", tags=["Admin Dashboard"])
api_router.include_router(admin_health_router, prefix="/admin", tags=["Admin Dashboard"])

# Admin Users
api_router.include_router(admin_users_list, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_detail, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_edit, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_suspend, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_delete, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_kyc, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_limits, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_notes, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_tags, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_balance, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_accounts, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_cards, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_security, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_sessions, prefix="/admin/users", tags=["Admin Users"])
api_router.include_router(admin_users_bulk, prefix="/admin/users", tags=["Admin Users"])

# Admin Transactions
from app.api.v1.endpoints.admin.transactions.list import router as admin_tx_list
from app.api.v1.endpoints.admin.transactions.detail import router as admin_tx_detail
from app.api.v1.endpoints.admin.transactions.approve import router as admin_tx_approve
from app.api.v1.endpoints.admin.transactions.reject import router as admin_tx_reject
from app.api.v1.endpoints.admin.transactions.reverse import router as admin_tx_reverse
from app.api.v1.endpoints.admin.transactions.flag import router as admin_tx_flag
from app.api.v1.endpoints.admin.transactions.bulk import router as admin_tx_bulk
from app.api.v1.endpoints.admin.transactions.export import router as admin_tx_export
api_router.include_router(admin_tx_list, prefix="/admin/transactions", tags=["Admin Transactions"])
api_router.include_router(admin_tx_detail, prefix="/admin/transactions", tags=["Admin Transactions"])
api_router.include_router(admin_tx_approve, prefix="/admin/transactions", tags=["Admin Transactions"])
api_router.include_router(admin_tx_reject, prefix="/admin/transactions", tags=["Admin Transactions"])
api_router.include_router(admin_tx_reverse, prefix="/admin/transactions", tags=["Admin Transactions"])
api_router.include_router(admin_tx_flag, prefix="/admin/transactions", tags=["Admin Transactions"])
api_router.include_router(admin_tx_bulk, prefix="/admin/transactions", tags=["Admin Transactions"])
api_router.include_router(admin_tx_export, prefix="/admin/transactions", tags=["Admin Transactions"])

# Admin Deposits
from app.api.v1.endpoints.admin.deposits.pending import router as admin_dep_pending
from app.api.v1.endpoints.admin.deposits.list import router as admin_dep_list
from app.api.v1.endpoints.admin.deposits.approve import router as admin_dep_approve
from app.api.v1.endpoints.admin.deposits.reject import router as admin_dep_reject
api_router.include_router(admin_dep_pending, prefix="/admin/deposits", tags=["Admin Deposits"])
api_router.include_router(admin_dep_list, prefix="/admin/deposits", tags=["Admin Deposits"])
api_router.include_router(admin_dep_approve, prefix="/admin/deposits", tags=["Admin Deposits"])
api_router.include_router(admin_dep_reject, prefix="/admin/deposits", tags=["Admin Deposits"])

# Admin Withdrawals
from app.api.v1.endpoints.admin.withdrawals.pending import router as admin_wth_pending
from app.api.v1.endpoints.admin.withdrawals.list import router as admin_wth_list
from app.api.v1.endpoints.admin.withdrawals.approve import router as admin_wth_approve
from app.api.v1.endpoints.admin.withdrawals.reject import router as admin_wth_reject
api_router.include_router(admin_wth_pending, prefix="/admin/withdrawals", tags=["Admin Withdrawals"])
api_router.include_router(admin_wth_list, prefix="/admin/withdrawals", tags=["Admin Withdrawals"])
api_router.include_router(admin_wth_approve, prefix="/admin/withdrawals", tags=["Admin Withdrawals"])
api_router.include_router(admin_wth_reject, prefix="/admin/withdrawals", tags=["Admin Withdrawals"])

from app.api.v1.endpoints.admin.methods.deposit_methods import router as admin_dep_methods
from app.api.v1.endpoints.admin.methods.withdrawal_methods import router as admin_wth_methods
from app.api.v1.endpoints.admin.methods.crypto_config import router as admin_crypto_cfg
from app.api.v1.endpoints.admin.methods.banking_details import router as admin_banking
api_router.include_router(admin_dep_methods, prefix="/admin/methods", tags=["Admin Methods"])
api_router.include_router(admin_wth_methods, prefix="/admin/methods", tags=["Admin Methods"])
api_router.include_router(admin_crypto_cfg, prefix="/admin/methods", tags=["Admin Methods"])
api_router.include_router(admin_banking, prefix="/admin/methods", tags=["Admin Methods"])

from app.api.v1.endpoints.admin.roles.list import router as roles_list
from app.api.v1.endpoints.admin.roles.create import router as roles_create
from app.api.v1.endpoints.admin.roles.edit import router as roles_edit
from app.api.v1.endpoints.admin.roles.delete import router as roles_delete
from app.api.v1.endpoints.admin.roles.clone import router as roles_clone
from app.api.v1.endpoints.admin.roles.permissions import router as roles_perms
from app.api.v1.endpoints.admin.permissions.list import router as perms_list
from app.api.v1.endpoints.admin.permissions.matrix import router as perms_matrix
from app.api.v1.endpoints.admin.admins.list import router as admins_list
from app.api.v1.endpoints.admin.admins.create import router as admins_create
from app.api.v1.endpoints.admin.admins.edit import router as admins_edit
from app.api.v1.endpoints.admin.admins.delete import router as admins_delete
from app.api.v1.endpoints.admin.admins.roles import router as admins_roles
from app.api.v1.endpoints.admin.admins.activity import router as admins_activity
api_router.include_router(roles_list, prefix="/admin/roles", tags=["Admin Roles"])
api_router.include_router(roles_create, prefix="/admin/roles", tags=["Admin Roles"])
api_router.include_router(roles_edit, prefix="/admin/roles", tags=["Admin Roles"])
api_router.include_router(roles_delete, prefix="/admin/roles", tags=["Admin Roles"])
api_router.include_router(roles_clone, prefix="/admin/roles", tags=["Admin Roles"])
api_router.include_router(roles_perms, prefix="/admin/roles", tags=["Admin Roles"])
api_router.include_router(perms_list, prefix="/admin/permissions", tags=["Admin Permissions"])
api_router.include_router(perms_matrix, prefix="/admin/permissions", tags=["Admin Permissions"])
api_router.include_router(admins_list, prefix="/admin/admins", tags=["Admin Management"])
api_router.include_router(admins_create, prefix="/admin/admins", tags=["Admin Management"])
api_router.include_router(admins_edit, prefix="/admin/admins", tags=["Admin Management"])
api_router.include_router(admins_delete, prefix="/admin/admins", tags=["Admin Management"])
api_router.include_router(admins_roles, prefix="/admin/admins", tags=["Admin Management"])
api_router.include_router(admins_activity, prefix="/admin/admins", tags=["Admin Management"])

from app.api.v1.endpoints.admin.fees.list import router as fees_list
from app.api.v1.endpoints.admin.fees.edit import router as fees_edit
from app.api.v1.endpoints.admin.fees.schedule import router as fees_create
from app.api.v1.endpoints.admin.interest.rates import router as interest_rates
from app.api.v1.endpoints.admin.cards.list import router as admin_cards_all
from app.api.v1.endpoints.admin.cards.issue import router as admin_cards_issue
from app.api.v1.endpoints.admin.cards.manage import router as admin_cards_manage
from app.api.v1.endpoints.admin.cards.limits import router as admin_cards_limits
api_router.include_router(fees_list, prefix="/admin/fees", tags=["Admin Fees"])
api_router.include_router(fees_edit, prefix="/admin/fees", tags=["Admin Fees"])
api_router.include_router(fees_create, prefix="/admin/fees", tags=["Admin Fees"])
api_router.include_router(interest_rates, prefix="/admin/interest", tags=["Admin Interest"])
api_router.include_router(admin_cards_all, prefix="/admin/cards", tags=["Admin Cards"])
api_router.include_router(admin_cards_issue, prefix="/admin/cards", tags=["Admin Cards"])
api_router.include_router(admin_cards_manage, prefix="/admin/cards", tags=["Admin Cards"])
api_router.include_router(admin_cards_limits, prefix="/admin/cards", tags=["Admin Cards"])

from app.api.v1.endpoints.admin.reports.builder import router as reports_builder
from app.api.v1.endpoints.admin.reports.list import router as reports_list
from app.api.v1.endpoints.admin.reports.generate import router as reports_save
from app.api.v1.endpoints.admin.reports.schedule import router as reports_schedule
from app.api.v1.endpoints.admin.audit.list import router as audit_list
from app.api.v1.endpoints.admin.audit.export import router as audit_export
api_router.include_router(reports_builder, prefix="/admin/reports", tags=["Admin Reports"])
api_router.include_router(reports_list, prefix="/admin/reports", tags=["Admin Reports"])
api_router.include_router(reports_save, prefix="/admin/reports", tags=["Admin Reports"])
api_router.include_router(reports_schedule, prefix="/admin/reports", tags=["Admin Reports"])
api_router.include_router(audit_list, prefix="/admin/audit", tags=["Admin Audit"])
api_router.include_router(audit_export, prefix="/admin/audit", tags=["Admin Audit"])

from app.api.v1.endpoints.admin.system.settings import router as sys_settings
from app.api.v1.endpoints.admin.system.email_templates import router as email_temps
from app.api.v1.endpoints.admin.system.sms_templates import router as sms_temps
from app.api.v1.endpoints.admin.system.push_templates import router as push_temps
from app.api.v1.endpoints.admin.system.legal import router as legal_docs
from app.api.v1.endpoints.admin.system.api_keys import router as api_keys
from app.api.v1.endpoints.admin.system.webhooks import router as webhooks
from app.api.v1.endpoints.admin.system.security import router as sys_security
from app.api.v1.endpoints.admin.system.kyc_settings import router as kyc_settings
from app.api.v1.endpoints.admin.notifications.send import router as admin_notif_send
from app.api.v1.endpoints.admin.notifications.templates import router as admin_notif_temps
from app.api.v1.endpoints.admin.notifications.history import router as admin_notif_hist
from app.api.v1.endpoints.admin.announcements.list import router as announce_list
from app.api.v1.endpoints.admin.announcements.create import router as announce_create
from app.api.v1.endpoints.admin.announcements.edit import router as announce_edit
api_router.include_router(sys_settings, prefix="/admin/system", tags=["Admin System"])
api_router.include_router(email_temps, prefix="/admin/system/email", tags=["Admin System"])
api_router.include_router(sms_temps, prefix="/admin/system/sms", tags=["Admin System"])
api_router.include_router(push_temps, prefix="/admin/system/push", tags=["Admin System"])
api_router.include_router(legal_docs, prefix="/admin/system/legal", tags=["Admin System"])
api_router.include_router(api_keys, prefix="/admin/system/api-keys", tags=["Admin System"])
api_router.include_router(webhooks, prefix="/admin/system/webhooks", tags=["Admin System"])
api_router.include_router(sys_security, prefix="/admin/system/security", tags=["Admin System"])
api_router.include_router(kyc_settings, prefix="/admin/system/kyc", tags=["Admin System"])
api_router.include_router(admin_notif_send, prefix="/admin/notifications", tags=["Admin Notifications"])
api_router.include_router(admin_notif_temps, prefix="/admin/notifications/templates", tags=["Admin Notifications"])
api_router.include_router(admin_notif_hist, prefix="/admin/notifications/history", tags=["Admin Notifications"])
api_router.include_router(announce_list, prefix="/admin/announcements", tags=["Admin Announcements"])
api_router.include_router(announce_create, prefix="/admin/announcements", tags=["Admin Announcements"])
api_router.include_router(announce_edit, prefix="/admin/announcements", tags=["Admin Announcements"])
