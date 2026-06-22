# Bank App â€” Admin Panel Integration Guide

> This document is for the **Admin Panel frontend** only.
> The user-facing app documentation is in `FRONTEND_README.md`.
> Phases covered: 14 (Auth & Dashboard) â€” more phases will be appended as they are completed.

---

## Quick Reference

| Item | Value |
|---|---|
| **Live API base URL** | `https://worldcup-orcin-chi.vercel.app` |
| **All admin API calls** | `https://worldcup-orcin-chi.vercel.app/api/v1/admin/...` |
| **Swagger UI** | `https://worldcup-orcin-chi.vercel.app/docs` |
| **ReDoc** | `https://worldcup-orcin-chi.vercel.app/redoc` |
| **OpenAPI JSON** | `https://worldcup-orcin-chi.vercel.app/openapi.json` |

Use Swagger at `/docs` to test every endpoint live in the browser before integrating.

---

## Standard Response Envelope

Every endpoint wraps its response in the same shape used by the user API:

```json
{
  "success": true,
  "message": "OK",
  "data": { ... }
}
```

On failure:
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

---

## Admin Authentication â€” How It Works

The admin system is **completely separate** from the user auth system. Admin tokens and user tokens are different JWTs and are not interchangeable.

### Token flow

1. `POST /api/v1/admin/auth/login` â†’ returns `access_token` + `refresh_token`
2. Send the access token on every protected admin request:
   ```
   Authorization: Bearer <admin_access_token>
   ```
3. Access token expires in **30 minutes** (same setting as user tokens)
4. Refresh token lives for **7 days**
5. `POST /api/v1/admin/auth/refresh` to get a new token pair

### Admin-specific JWT payload

Admin tokens include `"is_admin": true` and `"role": "admin"` in the payload, which is how the backend distinguishes admin requests from user requests.

### HTTP error codes

| Code | Meaning |
|---|---|
| `401` | Token missing, invalid, or expired â€” redirect to admin login |
| `403` | Admin account inactive or suspended |
| `422` | Validation error â€” show field errors |
| `500` | Server error |

---

## PHASE 14 â€” Admin Auth & Dashboard

### Base path: `/api/v1/admin/`

---

## 1. Admin Login

```
POST /api/v1/admin/auth/login
```

**No auth required.**

Request body:
```json
{
  "email": "admin@bankapp.com",
  "password": "your-admin-password"
}
```

Success response `data`:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "admin_id": "uuid",
  "full_name": "Super Admin",
  "email": "admin@bankapp.com",
  "is_super_admin": true,
  "permissions": []
}
```

> **`permissions` is currently an empty array `[]`** â€” the permission system model and tables are built but the service does not yet populate permissions on login. Build the UI to handle this gracefully. Permissions will be populated in a future phase as the RBAC system is completed.

**On successful login, store:**
- `access_token` â€” send as `Authorization: Bearer` on every request
- `refresh_token` â€” for token renewal
- `admin_id`, `full_name`, `email` â€” for display in the admin UI header
- `is_super_admin` â€” to conditionally show super-admin-only sections

**Failed login errors (in `message` field):**
- `"Invalid credentials"` â€” wrong email or password
- `"Invalid credentials"` â€” account inactive (same message for security â€” no info leak)

**Login activity is logged** â€” every successful login creates an `AdminActivityLog` record with action `"login"` and the request IP address.

---

## 2. Admin Logout

```
POST /api/v1/admin/auth/logout
Authorization: Bearer <admin_access_token>
```

No request body.

```json
{ "success": true, "message": "Logged out" }
```

> **Current state:** The logout endpoint returns success immediately â€” it does not currently invalidate the session in the database. The session row in `admin_sessions` is not marked `logged_out_at`. This means the token remains technically valid until it expires (30 min). Client-side: clear the stored token immediately on logout regardless. A proper session invalidation will be implemented in a future update.

---

## 3. Refresh Admin Token

```
POST /api/v1/admin/auth/refresh
Authorization: Bearer <admin_refresh_token>
```

No request body.

```json
{ "success": true, "message": "Token refreshed" }
```

> **Current state:** The refresh endpoint returns a success message but **does not return new tokens yet**. The token rotation logic is not implemented in this endpoint. As a workaround, when a 401 is received, redirect the admin to the login screen rather than attempting a silent refresh. This will be fully implemented in a future update.

---

## 4. Admin 2FA Verify

```
POST /api/v1/admin/auth/verify-2fa
Authorization: Bearer <temp_admin_token>
```

No request body in the current implementation.

```json
{ "success": true, "message": "2FA verified" }
```

> **Current state:** The 2FA verification endpoint is a stub â€” it returns success without actually verifying a TOTP code. The admin model has `two_fa_secret` and `is_2fa_enabled` fields ready, but the verification logic is not yet wired in. Do not build a 2FA entry screen for admins yet â€” skip this step in the login flow and go straight to the dashboard after password login.

---

## 5. Dashboard Statistics

```
GET /api/v1/admin/dashboard/stats
Authorization: Bearer <admin_access_token>
```

Returns live counts and totals from the database.

Success response `data`:
```json
{
  "total_users": 1482,
  "pending_deposits": 23,
  "pending_withdrawals": 8,
  "total_balance": 2847392.50
}
```

> **Note on missing fields:** The `DashboardStats` schema defines additional fields (`active_users`, `total_accounts`, `pending_kyc`, `deposits_today`, `withdrawals_today`) but the current service only returns `total_users`, `pending_deposits`, `pending_withdrawals`, and `total_balance`. The other fields will be populated as the backend adds the corresponding repository queries. Build the dashboard UI with all the schema fields visible but handle missing/null values gracefully â€” show `â€”` or `0` for fields not yet returned.

**Recommended dashboard cards:**

| Stat | Field | Icon |
|---|---|---|
| Total Users | `total_users` | ðŸ‘¥ |
| Active Users | `active_users` | *(not returned yet)* |
| Total Accounts | `total_accounts` | *(not returned yet)* |
| Pending Deposits | `pending_deposits` | â³ â†“ |
| Pending Withdrawals | `pending_withdrawals` | â³ â†‘ |
| Pending KYC | `pending_kyc` | *(not returned yet)* |
| Total Balance (all accounts) | `total_balance` | ðŸ’° |
| Deposits Today | `deposits_today` | *(not returned yet)* |
| Withdrawals Today | `withdrawals_today` | *(not returned yet)* |

---

## 6. System Health Check

```
GET /api/v1/admin/dashboard/health
```

**No auth required** â€” useful for uptime monitoring.

Success response `data`:
```json
{
  "database": "connected",
  "redis": "disabled",
  "status": "ok"
}
```

- `database: "connected"` â€” Neon PostgreSQL is reachable
- `redis: "disabled"` â€” Redis is not configured in the current deployment
- `status: "ok"` â€” overall system status

Use this endpoint for a status indicator in the admin panel header. Poll it every 30â€“60 seconds. If `status !== "ok"`, show a warning banner.

---

## Admin Data Model Reference

### Admin object fields

| Field | Type | Notes |
|---|---|---|
| `id` | string (UUID) | Admin unique ID |
| `email` | string | Login email â€” unique |
| `username` | string | 3â€“50 chars â€” unique |
| `full_name` | string | Display name |
| `role_id` | string (UUID) | FK to `admin_roles` table |
| `is_active` | bool | If false, login is blocked |
| `is_super_admin` | bool | Super admins bypass permission checks |
| `failed_login_attempts` | string | Count of consecutive failures |
| `locked_until` | datetime | Account locked until this time |
| `last_login_at` | datetime | Most recent login timestamp |
| `ip_whitelist` | string | Comma-separated IPs (optional restriction) |
| `working_hours_start` | string | e.g. `"09:00"` â€” optional time restriction |
| `working_hours_end` | string | e.g. `"17:00"` |
| `is_2fa_enabled` | bool | Whether 2FA is set up (not yet enforced) |

### Admin roles

Roles are stored in `admin_roles` with a `level` field:

| Level | Meaning |
|---|---|
| `1` | Super Admin â€” full access |
| `2` | Manager â€” most access |
| `3` | Operator â€” standard access (default) |

`is_system: "true"` marks built-in roles that cannot be deleted.

### Admin permissions

Permissions are stored as `permission_key` strings assigned to a role. They follow a `resource.action` pattern. Examples:

```
users.view          users.edit          users.suspend
deposits.approve    deposits.reject     deposits.view
withdrawals.approve withdrawals.reject
kyc.approve         kyc.reject
transactions.view   transactions.dispute
cards.freeze        cards.view
admins.create       admins.edit         admins.delete
reports.view        reports.export
```

> **Permissions are not yet enforced** on individual endpoints in Phase 14 â€” the middleware and permission check infrastructure exists (`app/middleware/permission_middleware.py`, `app/services/permission_service.py`) but is not wired into the dashboard and auth endpoints yet. All authenticated admins can access all Phase 14 endpoints regardless of their role. Permission enforcement will be activated as each admin module is implemented.

### Admin activity log

Every significant admin action is recorded in `admin_activity_logs`:

| Field | Description |
|---|---|
| `admin_id` | Who performed the action |
| `admin_name` | Display name at time of action |
| `action` | e.g. `"login"`, `"approve_deposit"`, `"suspend_user"` |
| `target_type` | e.g. `"user"`, `"deposit"`, `"withdrawal"` |
| `target_id` | UUID of the affected record |
| `details` | Free-text description |
| `ip_address` | Request IP |
| `before_value` | JSON snapshot before change |
| `after_value` | JSON snapshot after change |

---

## Creating the First Super Admin

Run the seed script on the server to create the initial super admin account:

```bash
python scripts/create_super_admin.py
```

Default credentials are set in `.env`:
```
SUPER_ADMIN_EMAIL=admin@bankapp.com
SUPER_ADMIN_PASSWORD=change-me-admin-password
```

**Change these immediately after first login.**

---

## Phase 14 Admin Screens to Build

- [ ] Admin Login page â€” email + password form
- [ ] Admin header â€” shows `full_name`, role badge, logout button
- [ ] Dashboard home â€” stat cards grid (handle nulls gracefully)
- [ ] System status indicator â€” health check badge in header/sidebar
- [ ] Token expiry handling â€” redirect to login on 401

---

## Key Notes for Phase 14

- **Admin tokens are separate from user tokens** â€” never send an admin token to a user endpoint or vice versa. Both use Bearer format but different JWT payloads.
- **`permissions` array is empty for now** â€” do not use it to gate UI sections yet. Show all admin sections to all authenticated admins until permission enforcement is implemented.
- **Logout does not invalidate the server-side session yet** â€” always clear the token client-side immediately on logout. Don't rely on server-side session kill.
- **Refresh token endpoint is a stub** â€” redirect to login on 401 rather than attempting silent refresh.
- **2FA endpoint is a stub** â€” skip the 2FA step in the login flow entirely for now.
- **Stats only returns 4 fields** â€” build all 9 cards from the schema but handle missing fields with `0` / `â€”` fallback.
- **`is_super_admin: true`** should show additional UI sections (admin management, system settings) that regular admins don't see. Gate these on the client using the `is_super_admin` value from the login response.
- **Health endpoint needs no auth** â€” use it for a status page or uptime monitor without requiring an admin token.

---

## Coming in Next Admin Phases

The following admin modules are already scaffolded in the codebase and will be documented as they are completed:

| Phase | Module |
|---|---|
| 15 | User management (view, edit, suspend, KYC approval) |
| 16 | Deposit approvals (approve / reject all 7 methods) |
| 17 | Withdrawal approvals |
| 18 | Transaction management & dispute resolution |
| 19 | Card management (freeze, cancel, replace) |
| 20 | Admin management (create, edit, roles, permissions) |
| 21 | Reports & analytics |
| 22 | System settings & configuration |
| 23 | Audit logs & compliance |
| 24 | Announcements & notifications |


---

## PHASE 15 â€” Admin User Management

> All Phase 15 endpoints: `https://worldcup-orcin-chi.vercel.app/api/v1/admin/users/...`
> All endpoints are currently **open** â€” no admin auth token required yet. Authentication middleware will be enforced in a future update. For now, any request reaches the endpoint.

---

### Endpoint Implementation Status

Before building, know which endpoints are fully implemented vs stubs:

| Endpoint | Status |
|---|---|
| `GET /admin/users/list` | âœ… Fully implemented |
| `GET /admin/users/{user_id}` | âœ… Fully implemented |
| `PUT /admin/users/{user_id}/edit` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/suspend` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/activate` | âœ… Fully implemented |
| `DELETE /admin/users/{user_id}` | âœ… Fully implemented (soft delete) |
| `PUT /admin/users/{user_id}/kyc` | âœ… Fully implemented |
| `PUT /admin/users/{user_id}/limits` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/notes` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/tags` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/balance` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/accounts` | âœ… Fully implemented |
| `POST /admin/users/accounts/{account_id}/freeze` | âœ… Fully implemented |
| `POST /admin/users/accounts/{account_id}/unfreeze` | âœ… Fully implemented |
| `POST /admin/users/cards/{card_id}/freeze` | âœ… Fully implemented |
| `POST /admin/users/cards/{card_id}/cancel` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/reset-password` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/reset-2fa` | âœ… Fully implemented |
| `POST /admin/users/{user_id}/force-logout` | âœ… Fully implemented |
| `POST /admin/users/bulk` | âœ… Fully implemented |
| `GET /admin/users/{user_id}/beneficiaries` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/linked_accounts` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/activity` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/notifications` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/support` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/documents` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/relationships` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/compliance` | âš ï¸ Stub â€” returns `[]` |
| `GET /admin/users/{user_id}/overrides` | âš ï¸ Stub â€” returns `[]` |

> **Stub endpoints** return `{ "success": true, "data": [] }` immediately with no DB query. Use the user detail endpoint (`GET /admin/users/{user_id}`) instead â€” it already embeds beneficiaries, linked accounts, activity, and documents directly. The stub endpoints will be fleshed out in a future update.

---

### 1. List Users

```
GET /api/v1/admin/users/list?page=1&per_page=20
```

Query params:

| Param | Type | Description |
|---|---|---|
| `page` | int â‰¥ 1 | Default `1` |
| `per_page` | int 1â€“100 | Default `20` |
| `search` | string | Searches email, username, first name, last name |
| `status` | string | `active`, `suspended`, `inactive` â€” omit for all |

Example:
```
GET /api/v1/admin/users/list?search=john&status=active&page=1&per_page=20
```

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "email": "john@example.com",
      "username": "johndoe",
      "phone": "5551234567",
      "is_active": true,
      "is_suspended": false,
      "kyc_status": "verified",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2026-06-01T08:00:00"
    }
  ],
  "total": 1482,
  "page": 1,
  "per_page": 20
}
```

> Deleted users (`is_deleted = true`) are automatically excluded from all list results.

---

### 2. User Full Detail

```
GET /api/v1/admin/users/{user_id}
```

The main endpoint for the user detail page. Returns everything in one call â€” profile, accounts, cards, KYC docs, sessions, devices, notes, tags, activity, login history, beneficiaries, linked accounts, recent deposits, and recent withdrawals.

Success response `data`:
```json
{
  "profile": {
    "id": "uuid",
    "email": "john@example.com",
    "username": "johndoe",
    "phone": "5551234567",
    "is_active": true,
    "is_suspended": false,
    "is_email_verified": true,
    "is_phone_verified": false,
    "is_2fa_enabled": false,
    "biometric_enabled": false,
    "kyc_status": "verified",
    "failed_login_attempts": 0,
    "last_login_at": "2026-06-20T10:30:00",
    "created_at": "2026-06-01T08:00:00"
  },
  "personal": {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "ssn_last_four": "6789",
    "address": "123 Main St, New York, NY 10001"
  },
  "accounts": [
    {
      "id": "uuid",
      "account_number": "4820193847261",
      "account_type": "checking",
      "balance": 2540.00,
      "available_balance": 2340.00,
      "is_frozen": false
    }
  ],
  "cards": [
    {
      "id": "uuid",
      "last_four": "4521",
      "card_type": "virtual",
      "status": "active",
      "is_frozen": false
    }
  ],
  "kyc_documents": [
    {
      "id": "uuid",
      "type": "driver_license",
      "status": "approved",
      "file_url": "/uploads/abc.jpg"
    }
  ],
  "sessions": [
    {
      "id": "uuid",
      "ip": "192.168.1.1",
      "device": "iPhone 15 Pro",
      "created": "2026-06-20T10:00:00"
    }
  ],
  "devices": [
    {
      "id": "uuid",
      "name": "iPhone 15 Pro",
      "last_used": "2026-06-20T10:00:00"
    }
  ],
  "notes": [
    {
      "id": "uuid",
      "note": "User flagged for review",
      "author": "Admin",
      "pinned": true,
      "created": "2026-06-15T09:00:00"
    }
  ],
  "tags": ["vip", "flagged"],
  "activity": [
    {
      "action": "login",
      "description": "Login from New York",
      "ip": "192.168.1.1",
      "time": "2026-06-20T10:00:00"
    }
  ],
  "login_history": [
    {
      "method": "password",
      "success": true,
      "ip": "192.168.1.1",
      "time": "2026-06-20T10:00:00"
    }
  ],
  "beneficiaries": [
    { "id": "uuid", "name": "Jane Doe", "account": "9876543210" }
  ],
  "linked_accounts": [
    { "id": "uuid", "bank": "Chase Bank", "verified": true }
  ],
  "recent_deposits": [
    {
      "id": "uuid",
      "amount": 1000.00,
      "method": "ach",
      "status": "approved",
      "ref": "DEP-B8L3N1"
    }
  ],
  "recent_withdrawals": [
    {
      "id": "uuid",
      "amount": 200.00,
      "method": "wire",
      "status": "pending",
      "ref": "WTH-X2K9P3"
    }
  ]
}
```

> **Limits:** `activity` returns last 20 entries, `login_history` returns last 10, `recent_deposits` returns last 10, `recent_withdrawals` returns last 10. These are not paginated in this endpoint â€” use the dedicated stub endpoints (or the user-side history endpoints) for full history.

---

### 3. Edit User

```
PUT /api/v1/admin/users/{user_id}/edit
```

Request body â€” all fields optional:
```json
{
  "email": "newemail@example.com",
  "username": "newusername",
  "phone": "5559876543",
  "first_name": "Johnny",
  "last_name": "Doe",
  "is_active": true
}
```

`first_name` and `last_name` update the `user_profiles` table. All other fields update the `users` table.

```json
{ "success": true, "message": "User updated" }
```

---

### 4. Suspend User

```
POST /api/v1/admin/users/{user_id}/suspend
```

No request body. Sets `is_suspended = true` and records `suspended_at` timestamp.

```json
{ "success": true, "message": "User suspended" }
```

> A suspended user gets a `403` on all their API calls â€” `get_current_user` blocks suspended accounts. Suspension takes effect on the next request after this call.

---

### 5. Activate User

```
POST /api/v1/admin/users/{user_id}/activate
```

No request body. Sets `is_suspended = false`, `is_active = true`, clears `suspended_at`.

```json
{ "success": true, "message": "User activated" }
```

---

### 6. Delete User

```
DELETE /api/v1/admin/users/{user_id}
```

**Soft delete** â€” sets `is_deleted = true`, `is_active = false`, records `deleted_at`. The record remains in the database. The user is excluded from all list queries automatically.

```json
{ "success": true, "message": "User deleted" }
```

> Show a confirmation dialog before calling this. There is no undo endpoint â€” deletion is permanent from the user's perspective even though the DB row stays.

---

### 7. KYC Approval / Rejection

```
PUT /api/v1/admin/users/{user_id}/kyc
```

Request body:
```json
{
  "status": "approved",
  "reason": ""
}
```

For rejection:
```json
{
  "status": "rejected",
  "reason": "ID document is blurry and unreadable. Please resubmit."
}
```

`status` values: `approved`, `rejected`, `pending`, `not_submitted`

- On `approved`: sets `kyc_verified_at` to now
- On `rejected`: stores `reason` in `kyc_rejection_reason` on the user record

```json
{ "success": true, "message": "KYC approved" }
```

The `reason` field is required when `status = "rejected"`. Enforce this on the frontend.

---

### 8. Override User Limits

```
PUT /api/v1/admin/users/{user_id}/limits
```

All fields optional â€” send only what you want to change:
```json
{
  "daily_deposit_limit": 50000.00,
  "daily_withdrawal_limit": 25000.00,
  "daily_transfer_limit": 50000.00,
  "per_transaction_limit": 20000.00,
  "card_spending_limit": 10000.00,
  "atm_withdrawal_limit": 2000.00
}
```

If no `UserLimit` record exists for the user, one is created automatically.

```json
{ "success": true, "message": "Limits updated" }
```

---

### 9. Add Internal Note

```
POST /api/v1/admin/users/{user_id}/notes
```

```json
{
  "note": "User called in regarding pending withdrawal. Verified identity. Proceeding with manual approval.",
  "is_pinned": true
}
```

- `note`: required, free text
- `is_pinned`: optional bool, default `false` â€” pinned notes appear at the top of the notes list

`author_name` is hardcoded as `"Admin"` â€” it will reflect the actual admin name once admin auth middleware is wired in.

Success response `data`:
```json
{ "id": "uuid" }
```

Notes appear in `GET /admin/users/{user_id}` â†’ `notes[]`.

---

### 10. Add Tag

```
POST /api/v1/admin/users/{user_id}/tags
```

```json
{
  "tag": "vip"
}
```

Tags are free-text strings. Suggested standard tags to use consistently:
`vip`, `flagged`, `high-risk`, `manual-review`, `fraud-suspect`, `locked`, `kyc-pending`, `whale`

Tags appear in `GET /admin/users/{user_id}` â†’ `tags[]` as a plain string array.

> There is no `DELETE /tags` endpoint yet â€” tags cannot be removed through the API. This will be added in a future update.

---

### 11. Adjust Account Balance

```
POST /api/v1/admin/users/{user_id}/balance
```

```json
{
  "account_id": "uuid-of-account",
  "amount": 500.00,
  "reason": "Goodwill credit for service outage"
}
```

- `amount`: positive float = **credit** (add money)
- `amount`: negative float = **debit** (remove money). Example: `-200.00`
- `account_id`: must belong to the specified `user_id`
- `reason`: optional, for audit trail (stored in `reason` field but not yet logged to activity log)

Both `balance` and `available_balance` are adjusted by the same amount simultaneously.

```json
{ "success": true, "message": "Balance adjusted by $500.00" }
```

> **No validation on negative balance** â€” the endpoint allows debiting more than the current balance, resulting in a negative balance. Validate on the frontend: check the current balance from user detail before submitting a debit.

---

### 12. Create Account for User

```
POST /api/v1/admin/users/{user_id}/accounts
```

No request body. Creates a savings account named `"Admin Created Savings"` with a generated account number.

Success response `data`:
```json
{
  "id": "uuid",
  "number": "5931820473652"
}
```

> Currently only creates savings accounts. Account type configuration will be added in a future update.

---

### 13. Freeze / Unfreeze Account

```
POST /api/v1/admin/users/accounts/{account_id}/freeze
POST /api/v1/admin/users/accounts/{account_id}/unfreeze
```

> âš ï¸ **URL note:** These endpoints use `account_id` directly â€” not nested under a `user_id`. There is no user ownership check in the current implementation. Any account ID can be frozen/unfrozen by any admin.

No request body.

```json
{ "success": true, "message": "Account frozen" }
{ "success": true, "message": "Account unfrozen" }
```

---

### 14. Freeze Card

```
POST /api/v1/admin/users/cards/{card_id}/freeze
```

No request body. Sets `is_frozen = true`.

```json
{ "success": true, "message": "Card frozen" }
```

---

### 15. Cancel Card

```
POST /api/v1/admin/users/cards/{card_id}/cancel
```

No request body. Sets `status = "cancelled"` and `is_deleted = true`. Permanent â€” no reactivation.

```json
{ "success": true, "message": "Card cancelled" }
```

> Show a confirmation dialog. This is irreversible.

---

### 16. Reset User Password

```
POST /api/v1/admin/users/{user_id}/reset-password
```

No request body. Sets the user's password to `TempPass123!`.

```json
{ "success": true, "message": "Password reset to TempPass123!" }
```

> **The temporary password is always `TempPass123!`** â€” this is hardcoded in the current implementation. After calling this, inform the user through a separate channel (email/SMS) that their password has been reset and they must change it on next login. A configurable temp password or email-based reset link will be implemented in a future update.

---

### 17. Reset User 2FA

```
POST /api/v1/admin/users/{user_id}/reset-2fa
```

No request body. Sets `is_2fa_enabled = false` and clears `two_fa_secret`.

```json
{ "success": true, "message": "2FA reset" }
```

The user will need to set up 2FA again from scratch after this.

---

### 18. Force Logout User

```
POST /api/v1/admin/users/{user_id}/force-logout
```

No request body. Terminates **all active sessions** for the user by setting `is_active = false` and `logged_out_at = now()` on every active `UserSession` row.

```json
{ "success": true, "message": "All sessions terminated" }
```

The user's existing access tokens remain technically valid until they expire (30 min) but their sessions are marked inactive. A full token blacklist will enforce immediate invalidation in a future update.

---

### 19. Bulk Operations

```
POST /api/v1/admin/users/bulk
```

Apply one action to multiple users at once.

Request body:
```json
{
  "user_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "action": "suspend",
  "value": ""
}
```

`action` values:

| Action | Effect | `value` |
|---|---|---|
| `suspend` | Sets `is_suspended = true` on each user | Not used |
| `activate` | Sets `is_suspended = false`, `is_active = true` | Not used |
| `tag` | Adds a tag to each user | The tag string e.g. `"flagged"` |
| `delete` | Soft-deletes each user | Not used |

Users that don't exist are silently skipped â€” the operation continues for the remaining IDs.

```json
{ "success": true, "message": "Bulk suspend completed for 3 users" }
```

> **No rollback on partial failure** â€” if one user doesn't exist, the rest still get processed. The response always returns success once the loop completes.

---

### User Detail Page â€” Recommended Layout

Build the user detail page as a tabbed or sectioned layout. All data comes from the single `GET /admin/users/{user_id}` call:

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [Profile Header]                                           â”‚
â”‚  Avatar | Full Name | Email | Status badge | KYC badge      â”‚
â”‚  [Suspend] [Activate] [Reset Password] [Force Logout]        â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ PROFILE    â”‚ Personal info, address, SSN last 4, DOB         â”‚
â”‚ ACCOUNTS   â”‚ Account cards with balances, freeze buttons     â”‚
â”‚ CARDS      â”‚ Card list with status, freeze/cancel buttons    â”‚
â”‚ KYC        â”‚ Document thumbnails, approve/reject buttons     â”‚
â”‚ SECURITY   â”‚ 2FA status, reset 2FA, failed login count       â”‚
â”‚ SESSIONS   â”‚ Active sessions list, force logout button       â”‚
â”‚ NOTES      â”‚ Internal notes with add note form               â”‚
â”‚ TAGS       â”‚ Tag chips with add tag form                     â”‚
â”‚ LIMITS     â”‚ Editable limit fields                           â”‚
â”‚ BALANCE    â”‚ Credit/Debit form per account                   â”‚
â”‚ ACTIVITY   â”‚ Last 20 activity log entries                    â”‚
â”‚ LOGIN LOG  â”‚ Last 10 login attempts                          â”‚
â”‚ DEPOSITS   â”‚ Last 10 deposits with approve/reject links      â”‚
â”‚ WITHDRAWALSâ”‚ Last 10 withdrawals with approve/reject links   â”‚
â”‚ BENEFICIAR.â”‚ (Stub â€” shows empty)                            â”‚
â”‚ LINKED ACC.â”‚ (Stub â€” shows empty)                            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

### Phase 15 Admin Screens to Build

- [ ] Users list page â€” searchable, filterable, paginated table
- [ ] User detail page â€” full tabbed/sectioned view
- [ ] Edit user modal â€” inline form for editable fields
- [ ] Suspend / Activate confirmation dialog
- [ ] Delete user confirmation dialog (hard warning)
- [ ] KYC review section â€” document thumbnails, approve / reject with reason
- [ ] Limits override form â€” per-field editable with save button
- [ ] Balance adjustment form â€” amount (positive/negative), account selector, reason
- [ ] Add note form â€” text area + pin toggle
- [ ] Add tag input â€” with suggested tag chips
- [ ] Account freeze/unfreeze toggle
- [ ] Card freeze / cancel buttons with confirmation
- [ ] Reset password confirmation dialog (shows temp password)
- [ ] Reset 2FA confirmation dialog
- [ ] Force logout confirmation dialog
- [ ] Bulk operations â€” select multiple users + action dropdown

---

### Key Notes for Phase 15

- **No auth enforcement on any of these endpoints yet** â€” they are publicly accessible. Do not expose the admin panel URL publicly until auth middleware is wired in. Restrict access by other means (IP allowlist, VPN, etc.) in the meantime.
- **User detail is a single large call** â€” don't make 15 separate API calls to build the detail page. One `GET /admin/users/{user_id}` gives you everything. The stub endpoints exist but return empty arrays.
- **Balance debit has no floor** â€” can go negative. Validate `amount >= -currentBalance` before allowing a debit submission.
- **Reset password is always `TempPass123!`** â€” communicate this to any admin using the panel. Never show this to the end user through the admin UI â€” send it via a separate out-of-band channel.
- **Account/card freeze URLs use the resource ID directly** (`/accounts/{account_id}/freeze`) not nested under a user â€” no user ownership check. Keep account/card IDs from the user detail response to ensure you're acting on the right user's resources.
- **Bulk tag requires `value`** â€” the `value` field is the tag string. For all other bulk actions, `value` can be empty string `""` or omitted.
- **`tags` in user detail is a plain string array** â€” e.g. `["vip", "flagged"]`. No tag IDs are returned, so there's no removal endpoint that takes an ID. Tag removal will require a future endpoint.
- **Suspend takes effect on the user's next API call** â€” it's not a real-time disconnect. Use force-logout together with suspend for immediate effect.
- **`beneficiaries`, `linked_accounts`, `activity`, `notifications`, `support`, `documents`, `relationships`, `compliance`, `overrides` endpoints are all stubs** â€” they return empty arrays. The user detail endpoint already embeds beneficiaries, linked accounts, and activity (last 20) â€” use that data instead.


---

## PHASE 16 â€” Admin Transactions & Approvals

> Base paths:
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/transactions/...`
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/deposits/...`
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/withdrawals/...`
>
> All endpoints are currently open â€” no admin auth token required yet.

---

### Two Approval Systems â€” Use the Right One

Phase 16 has two parallel approval systems. Know which to use:

| System | When to use | URL prefix |
|---|---|---|
| **Deposits/Withdrawals direct** | Approving/rejecting from the dedicated deposit or withdrawal queues | `/admin/deposits/` `/admin/withdrawals/` |
| **Transactions generic** | Approving/rejecting from the unified transaction list | `/admin/transactions/` |

**Use the deposit/withdrawal endpoints for the approval queues** â€” they are simpler, use the deposit/withdrawal `id` directly, and do the correct balance update.

**Use the transaction endpoints for the unified transaction history view** â€” they work via `transaction_id` from the central `transactions` table and also do balance updates, but only when `transaction_type` starts with `"deposit_"` or `"withdrawal_"`.

---

### What Approval Actually Does

**Approving a deposit:**
1. Sets `deposit.status = "completed"`
2. Stores `admin_notes` on the deposit record
3. Credits `account.balance += deposit.amount`
4. Credits `account.available_balance += deposit.amount`
5. Sets the linked `transaction.status = "completed"`

**Approving a withdrawal:**
1. Sets `withdrawal.status = "completed"`
2. Debits `account.balance -= withdrawal.amount`
3. Debits `account.available_balance -= withdrawal.amount`
4. Sets the linked `transaction.status = "completed"`

> **Note on withdrawal balance:** At the time a withdrawal is submitted by the user, `available_balance` is immediately reduced (to prevent double-spending). When the admin approves, `balance` is reduced to match. When the admin rejects â€” **neither balance field is restored in the current implementation.** The user's `available_balance` stays reduced even after a rejection. This is a known gap. Until it is fixed, after rejecting a withdrawal you should manually credit the `available_balance` back using the balance adjustment endpoint: `POST /admin/users/{user_id}/balance` with the withdrawal amount as a positive value. Flag this to the user through a notification.

---

### Endpoint Implementation Status

| Endpoint | Status | Notes |
|---|---|---|
| `GET /admin/transactions/list` | âœ… Full | Filters: type, status, user_id, search, dates |
| `GET /admin/transactions/{tx_id}` | âœ… Full | Full transaction detail |
| `POST /admin/transactions/approve` | âœ… Full | Credits balance for deposits, debits for withdrawals |
| `POST /admin/transactions/reject` | âœ… Full | Sets status; no balance restoration |
| `POST /admin/transactions/reverse` | âœ… Full | Only reverses `status=completed` transactions |
| `POST /admin/transactions/flag` | âš ï¸ Partial | Flag works; unflag does not restore original status |
| `POST /admin/transactions/bulk` | âœ… Full | Approve/reject on deposits only in bulk |
| `GET /admin/transactions/export/csv` | âœ… Full | No filters â€” always dumps latest 5000 rows |
| `GET /admin/deposits/pending` | âœ… Full | Paginated pending deposit queue |
| `GET /admin/deposits/list` | âœ… Full | All deposits, filterable by status |
| `POST /admin/deposits/{id}/approve` | âœ… Full | Credits balance + sets status |
| `POST /admin/deposits/{id}/reject` | âš ï¸ Partial | Sets status; no rejection reason stored; no balance restore |
| `GET /admin/withdrawals/pending` | âœ… Full | Paginated pending withdrawal queue |
| `GET /admin/withdrawals/list` | âœ… Full | All withdrawals, filterable by status |
| `POST /admin/withdrawals/{id}/approve` | âœ… Full | Debits balance + sets status |
| `POST /admin/withdrawals/{id}/reject` | âš ï¸ Partial | Sets status; no balance restore; no reason stored |

---

## SECTION A â€” Deposit Management

### A1. Pending Deposits Queue

```
GET /api/v1/admin/deposits/pending?page=1&per_page=20
```

The primary approval queue. Returns all deposits with `status = "pending"`, newest first.

Query params: `page` (default 1), `per_page` (1â€“100, default 20)

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "method": "ach",
      "amount": 1000.00,
      "fee": 0.00,
      "status": "pending",
      "reference": "DEP-B8L3N1",
      "created_at": "2026-06-20T14:30:00"
    },
    {
      "id": "uuid",
      "user_id": "uuid",
      "method": "crypto_eth",
      "amount": 5000.00,
      "fee": 0.00,
      "status": "pending",
      "reference": "DEP-X7K2M9",
      "created_at": "2026-06-20T13:15:00"
    }
  ],
  "total": 23,
  "page": 1
}
```

Use `user_id` to link to the user detail page (`GET /admin/users/{user_id}`).

> **Polling:** The dashboard stats endpoint (`GET /admin/dashboard/stats`) returns `pending_deposits` count. Poll that every 60 seconds and update a badge on the deposits nav item. When the badge is non-zero, the admin knows to check this queue.

### A2. All Deposits List

```
GET /api/v1/admin/deposits/list?page=1&per_page=20&status=pending
```

Query params:

| Param | Description |
|---|---|
| `page` | Default 1 |
| `per_page` | 1â€“100, default 20 |
| `status` | `pending`, `completed`, `rejected` â€” omit for all |

Response shape is the same as the pending queue but without the `fee` field.

### A3. Approve Deposit

```
POST /api/v1/admin/deposits/{deposit_id}/approve
```

No request body. Uses the deposit's own `id` (UUID from the list).

```json
{ "success": true, "message": "Deposit approved" }
```

**Effect:** `deposit.status â†’ "completed"` + `account.balance += amount` + `account.available_balance += amount`

> After approving, the user's balance is immediately updated. If the user is online, their next account balance request will reflect the new amount.

### A4. Reject Deposit

```
POST /api/v1/admin/deposits/{deposit_id}/reject
```

No request body.

```json
{ "success": true, "message": "Deposit rejected" }
```

**Effect:** `deposit.status â†’ "rejected"` only. No other changes.

> **Known gaps on deposit rejection:**
> 1. No `reason` field â€” the current endpoint takes no request body. There is nowhere to store a rejection reason at the deposit level. Use the balance adjustment or notes endpoint to communicate the reason on the user's record until this is fixed.
> 2. Crypto deposits that were pending in a `DepositSession` â€” the session record is not updated on deposit rejection. The session may still show `status: "pending"` on the user side.

---

## SECTION B â€” Withdrawal Management

### B1. Pending Withdrawals Queue

```
GET /api/v1/admin/withdrawals/pending?page=1&per_page=20
```

All withdrawals with `status = "pending"`, newest first.

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "method": "wire",
      "amount": 10000.00,
      "fee": 0.00,
      "status": "pending",
      "reference": "WTH-X2L8Q5",
      "created_at": "2026-06-20T12:00:00"
    }
  ],
  "total": 8
}
```

> `method_data` (which contains destination bank details, crypto address, etc.) is not returned in the list. To see the full details the user submitted, go to the user detail page and check `recent_withdrawals`, or implement a withdrawal detail endpoint in a future update. For now, use the `reference` to match the withdrawal to a user's request details stored in `method_data`.

### B2. All Withdrawals List

```
GET /api/v1/admin/withdrawals/list?page=1&per_page=20&status=pending
```

Same query params as deposits list. Filterable by `status`.

### B3. Approve Withdrawal

```
POST /api/v1/admin/withdrawals/{wid}/approve
```

No request body.

```json
{ "success": true, "message": "Withdrawal approved" }
```

**Effect:** `withdrawal.status â†’ "completed"` + `account.balance -= amount` + `account.available_balance -= amount`

> The `available_balance` was already reduced when the user submitted. This approval reduces `balance` to match â€” the net effect is both fields are now correctly reduced.

### B4. Reject Withdrawal

```
POST /api/v1/admin/withdrawals/{wid}/reject
```

No request body.

```json
{ "success": true, "message": "Withdrawal rejected" }
```

**Effect:** `withdrawal.status â†’ "rejected"` only.

> âš ï¸ **The available_balance is NOT restored on rejection.** The user's funds remain locked even after rejection. This is a backend bug. Until it is fixed:
> 1. After calling reject, immediately call `POST /admin/users/{user_id}/balance` with a positive `amount` equal to the withdrawal amount to manually restore the funds.
> 2. Add an internal note on the user explaining the manual adjustment.
> 3. Consider showing a warning in the reject confirmation dialog: "Remember to manually restore the user's available balance."

---

## SECTION C â€” Unified Transaction Management

### C1. List All Transactions

```
GET /api/v1/admin/transactions/list
```

Query params:

| Param | Type | Description |
|---|---|---|
| `page` | int â‰¥ 1 | Default 1 |
| `per_page` | int 1â€“100 | Default 20 |
| `transaction_type` | string | Filter by type â€” see values below |
| `status` | string | `pending`, `completed`, `rejected`, `reversed`, `flagged` |
| `user_id` | string (UUID) | Filter by specific user |
| `search` | string | Searches `description` and `reference` fields |
| `start_date` | string | ISO datetime `"2026-06-01T00:00:00"` â€” inclusive |
| `end_date` | string | ISO datetime `"2026-06-30T23:59:59"` â€” inclusive |

Example:
```
GET /api/v1/admin/transactions/list?status=pending&user_id=uuid&start_date=2026-06-01T00:00:00
```

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "transaction_type": "deposit_ach",
      "amount": 1000.00,
      "fee": 0.00,
      "net_amount": 1000.00,
      "status": "pending",
      "reference": "DEP-B8L3N1",
      "description": "ACH deposit",
      "user_id": "uuid",
      "created_at": "2026-06-20T14:30:00"
    }
  ],
  "total": 847,
  "page": 1,
  "per_page": 20
}
```

> **`transaction_type` format in this table** uses underscore-prefixed subtypes (e.g. `deposit_ach`, `withdrawal_wire`, `transfer_internal`). This is different from the user-facing transaction types. The approve/reject logic checks `transaction_type.startswith("deposit_")` or `startswith("withdrawal_")` â€” so only transactions with these prefixes trigger balance changes.

### C2. Transaction Detail

```
GET /api/v1/admin/transactions/{tx_id}
```

Returns the full transaction record:

```json
{
  "id": "uuid",
  "transaction_type": "deposit_ach",
  "amount": 1000.00,
  "fee": 0.00,
  "net_amount": 1000.00,
  "status": "pending",
  "reference": "DEP-B8L3N1",
  "description": "ACH deposit",
  "source": "ach",
  "recipient": null,
  "user_id": "uuid",
  "account_id": "uuid",
  "created_at": "2026-06-20T14:30:00"
}
```

### C3. Approve Transaction

```
POST /api/v1/admin/transactions/approve
```

Request body:
```json
{
  "transaction_id": "uuid",
  "notes": "Verified ACH transfer from Chase Bank statement."
}
```

- `transaction_id`: UUID from the transactions list
- `notes`: optional â€” stored in `deposit.admin_notes` or `withdrawal.admin_notes`

**Balance effect:**
- `transaction_type` starts with `"deposit_"` â†’ credits account balance
- `transaction_type` starts with `"withdrawal_"` â†’ debits account balance
- Any other type â†’ sets status only, no balance change

```json
{ "success": true, "message": "Transaction approved" }
```

### C4. Reject Transaction

```
POST /api/v1/admin/transactions/reject
```

Request body:
```json
{
  "transaction_id": "uuid",
  "reason": "Unable to verify source of funds."
}
```

`reason` is stored in `deposit.admin_notes` or `withdrawal.admin_notes` (for deposits/withdrawals). For other transaction types, the reason is not persisted anywhere.

> Same available_balance restoration issue applies here for withdrawals â€” see Section B4.

```json
{ "success": true, "message": "Transaction rejected" }
```

### C5. Reverse Transaction

```
POST /api/v1/admin/transactions/reverse
```

Request body:
```json
{
  "transaction_id": "uuid",
  "reason": "Duplicate transaction â€” user was charged twice."
}
```

**Only works on `status = "completed"` transactions.** Will return an error for pending or already-rejected transactions.

**Balance effect on reversal:**
- Deposit reversal â†’ debits account (`balance -= amount`, `available_balance -= amount`)
- Withdrawal reversal â†’ credits account (`balance += amount`, `available_balance += amount`)
- Any other type â†’ credits account

> **`reason` is not persisted** â€” the field is accepted but not stored anywhere in the current implementation. Log it manually as a note on the user record (`POST /admin/users/{user_id}/notes`) for audit purposes.

```json
{ "success": true, "message": "Transaction reversed" }
```

Sets `transaction.status = "reversed"`.

### C6. Flag / Unflag Transaction

```
POST /api/v1/admin/transactions/flag
```

Request body:
```json
{
  "transaction_id": "uuid",
  "flag": true
}
```

- `flag: true` â†’ sets `transaction.status = "flagged"`
- `flag: false` â†’ **does not restore the previous status** â€” the current code has a logic gap where unflagging skips the status change. The response says "Flag removed" but the status remains `"flagged"`.

> **Unflagging is broken.** Until fixed, to unflag a transaction manually approve or reject it which will overwrite the `"flagged"` status. Don't show the unflag option in the UI until this is resolved, or show it as a workaround that requires re-approval.

```json
{ "success": true, "message": "Transaction flagged" }
```

### C7. Bulk Operations

```
POST /api/v1/admin/transactions/bulk
```

Request body:
```json
{
  "transaction_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "action": "approve"
}
```

`action` values: `approve`, `reject`

**Bulk approve only processes deposits** â€” the current implementation only credits balance for `deposit_`-type transactions in bulk. Withdrawals in the batch are ignored for balance changes even on approve.

**Bulk reject** sets all listed transactions to `"rejected"` and updates linked deposits to `"rejected"`. No balance restoration.

Non-existent IDs are silently skipped.

```json
{ "success": true, "message": "Bulk approve completed" }
```

> Use bulk approve for processing a batch of crypto deposits after on-chain confirmations. Use it sparingly â€” there is no preview or confirmation step in the current implementation.

### C8. Export Transactions CSV

```
GET /api/v1/admin/transactions/export/csv
```

No query params â€” no filters. Always exports the latest **5,000 transactions** regardless of any filter you might want to apply.

Returns a raw CSV file download:
- `Content-Type: text/csv`
- `Content-Disposition: attachment; filename=transactions.csv`

CSV columns: `id`, `type`, `amount`, `fee`, `net`, `status`, `reference`, `description`, `user_id`, `created_at`

```javascript
// Trigger download
const response = await fetch('/api/v1/admin/transactions/export/csv', {
  headers: { 'Authorization': 'Bearer ' + adminToken }
});
const blob = await response.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url; a.download = 'transactions.csv'; a.click();
URL.revokeObjectURL(url);
```

> **Filters not supported yet.** The export always dumps the 5000 most recent rows. Date-range and status filtering will be added in a future update.

---

## Approval Workflow UX

### Recommended pending queue view

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  PENDING DEPOSITS  [23]          PENDING WITHDRAWALS  [8]    â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Reference    User       Method     Amount    Submitted       â”‚
â”‚  DEP-B8L3N1   John Doe   ACH        $1,000    2 hours ago    â”‚
â”‚  DEP-X7K2M9   Jane S.    Crypto ETH $5,000    3 hours ago    â”‚
â”‚                                               [âœ“] [âœ—]        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Each row should deep-link to the user detail page via `user_id`.
`[âœ“]` calls approve. `[âœ—]` calls reject with a reason modal.

### Deposit approve/reject flow

```
1. Admin sees pending deposit in queue
2. Taps row â†’ modal shows deposit details + user info
3. Taps "Approve" â†’ POST /admin/deposits/{id}/approve
        â†“ success
4. Remove item from queue (optimistic UI)
5. Show success toast "Deposit approved â€” $1,000 credited to user"

OR

3. Taps "Reject" â†’ reason input modal
4. Enter reason (inform user why)
5. POST /admin/deposits/{id}/reject
   (Then: POST /admin/users/{user_id}/notes with the reason text)
        â†“ success
6. Remove from queue
```

### Withdrawal approve/reject flow

```
1. Admin sees pending withdrawal
2. Taps row â†’ modal shows withdrawal details including method_data notes
   (crypto address / bank routing / etc. stored in notes field)
3. Taps "Approve" â†’ POST /admin/withdrawals/{id}/approve
        â†“ success
4. Process the actual money movement manually (wire, crypto send, etc.)
5. Show success toast

OR

3. Taps "Reject" â†’ reason input modal
4. POST /admin/withdrawals/{id}/reject
5. âš ï¸ IMMEDIATELY call POST /admin/users/{user_id}/balance
   with amount = withdrawal.amount (positive, to restore available_balance)
6. POST /admin/users/{user_id}/notes with explanation
```

---

## Phase 16 Admin Screens to Build

- [ ] Deposits pending queue â€” table with approve/reject buttons per row
- [ ] Withdrawals pending queue â€” table with approve/reject + method details
- [ ] Deposit approve confirmation dialog
- [ ] Deposit reject modal â€” reason text entry
- [ ] Withdrawal approve confirmation dialog
- [ ] Withdrawal reject modal â€” reason text entry + balance restore reminder
- [ ] All deposits list â€” filterable by status
- [ ] All withdrawals list â€” filterable by status
- [ ] Unified transaction history table â€” all filters (type, status, user, date range, search)
- [ ] Transaction detail modal â€” full fields + action buttons
- [ ] Approve transaction button (with notes field)
- [ ] Reject transaction button (with reason field)
- [ ] Reverse transaction button (completed transactions only) + confirmation
- [ ] Flag transaction button
- [ ] Bulk select + bulk approve/reject
- [ ] CSV export button

---

## Key Notes for Phase 16

- **Use deposit/withdrawal endpoints for the queues, transaction endpoint for the history table.** They are separate systems with overlapping functionality.
- **Deposit approval credits balance. Withdrawal approval debits balance.** Both happen at approval time, not at submission time.
- **Withdrawal rejection does not restore available_balance** â€” manual balance adjustment required. Show a warning in the UI and prompt the admin to do it.
- **Deposit rejection has no `reason` field** â€” use notes endpoint as a workaround. A `reason` body param will be added in a future update.
- **Transaction-level approve/reject only fires balance logic for `transaction_type` starting with `"deposit_"` or `"withdrawal_"`** â€” bare `"deposit"` or `"withdrawal"` types won't trigger balance changes through the transaction endpoint. Use the dedicated deposit/withdrawal endpoints for those.
- **Reversal reason is not persisted** â€” always follow a reversal with a manual note on the user record.
- **Flag â†’ unflag is broken** â€” unflagging sets `flag: false` in the request but the code skips the status update. The `"flagged"` status stays. Workaround: approve the transaction to clear the flag.
- **Bulk approve only fully processes deposits** â€” withdrawal balance deduction in bulk is not implemented. Use individual approval for withdrawals.
- **CSV export always exports 5000 rows, no filters** â€” if you need filtered data, use the list endpoint and build your own export on the frontend from the paginated results.
- **`start_date` / `end_date` in the transaction list accept ISO datetime strings** â€” include the time component: `"2026-06-01T00:00:00"` not just `"2026-06-01"`.
- **No `method_data` in withdrawal list/pending responses** â€” the destination details (crypto address, bank info, etc.) are stored in `method_data` on the withdrawal record but not returned in these endpoints. Access them via the user detail page's `recent_withdrawals` section for now.


---



---

## PHASE 17 — Admin Method Configuration

> Base path: `https://worldcup-orcin-chi.vercel.app/api/v1/admin/methods/...`

---

### Router Status — Important

All four Phase 17 endpoint files have working code written. **None of them are imported or registered in `router.py` yet** — they will all return 404 until the router is updated. The deposit_methods, crypto_config, and banking_details files are fully implemented. The withdrawal_methods.py file is 0 bytes on disk (empty).

| Endpoint file | Code written | Registered in router | Callable now |
|---|---|---|---|
| `deposit_methods.py` | ✅ | ❌ | ❌ 404 |
| `crypto_config.py` | ✅ | ❌ | ❌ 404 |
| `banking_details.py` | ✅ | ❌ | ❌ 404 |
| `withdrawal_methods.py` | ❌ empty | ❌ | ❌ 404 |

Build the admin UI for these now — the backend just needs a router update to make them live.

---

### 17.1 Deposit Methods Configuration

Once registered, URLs will be:
```
GET  /api/v1/admin/methods/deposit
PUT  /api/v1/admin/methods/deposit/{method_id}
```

**GET** — returns all deposit methods ordered by `display_order`:

```json
[
  {
    "id": "uuid",
    "name": "Crypto",
    "slug": "crypto",
    "is_enabled": true,
    "is_live": false,
    "min_amount": 0.01,
    "max_amount": 1000000.0,
    "fee_type": "flat",
    "fee_amount": 0.0,
    "processing_time": "1-3 business days",
    "display_order": "1",
    "requires_admin_approval": true
  },
  {
    "id": "uuid",
    "name": "ACH Transfer",
    "slug": "ach",
    "is_enabled": true,
    "is_live": false,
    "min_amount": 1.0,
    "max_amount": 10000.0,
    "fee_type": "flat",
    "fee_amount": 0.0,
    "processing_time": "2-3 business days",
    "display_order": "2",
    "requires_admin_approval": true
  }
]
```

**PUT `/{method_id}`** — update any fields on a single method. All fields optional:

```json
{
  "is_enabled": false,
  "is_live": true,
  "min_amount": 10.00,
  "max_amount": 50000.00,
  "fee_type": "flat",
  "fee_amount": 5.00,
  "processing_time": "Same day",
  "instructions": "Send wire to BankApp National, Routing 021000021, Account 4892736501. Include your DEP-XXXXXX reference in the memo field.",
  "display_order": "1",
  "requires_admin_approval": false
}
```

**What each field controls:**

| Field | Effect |
|---|---|
| `is_enabled` | `true` = shown in user app deposit picker. `false` = hidden immediately |
| `is_live` | Informational flag — marks real money movement vs simulation. Not enforced currently |
| `min_amount` / `max_amount` | Enforce deposit limits. User app reads these from `GET /deposits/methods` |
| `fee_type` | `"flat"` (fixed dollar) or `"percent"` (percentage of amount) |
| `fee_amount` | Fee value. Currently shown in UI but not enforced on deposits |
| `instructions` | Free text shown to users when they select this method. Wire and direct deposit methods must have accurate banking details here |
| `display_order` | String number — lower = shown first in the user's method list |
| `requires_admin_approval` | `true` = deposits go into pending queue. `false` = auto-approved (not recommended) |

> Changes to `is_enabled`, `min_amount`, `max_amount`, and `instructions` are reflected immediately on the user side — the user app's `GET /deposits/methods` reads directly from this table.

---

### 17.2 Crypto Network Configuration

```
GET  /api/v1/admin/methods/crypto
PUT  /api/v1/admin/methods/crypto/{network_id}
```

**GET** — all supported crypto networks, ordered by name:

```json
[
  {
    "id": "uuid",
    "name": "Bitcoin",
    "symbol": "BTC",
    "slug": "btc",
    "admin_wallet_address": "bc1qadminbitcoinaddressplaceholder",
    "is_enabled": true,
    "min_confirmations": "3",
    "contract_address": null
  },
  {
    "id": "uuid",
    "name": "Ethereum",
    "symbol": "ETH",
    "slug": "eth",
    "admin_wallet_address": "0x742d35Cc6634C0539085a3c1E39c7f5eC5D8d9a1",
    "is_enabled": true,
    "min_confirmations": "12",
    "contract_address": null
  },
  {
    "id": "uuid",
    "name": "USD Coin",
    "symbol": "USDC",
    "slug": "usdc_erc20",
    "admin_wallet_address": "0x742d35Cc6634C0539085a3c1E39c7f5eC5D8d9a1",
    "is_enabled": true,
    "min_confirmations": "12",
    "contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
  },
  {
    "id": "uuid",
    "name": "Tether USD",
    "symbol": "USDT",
    "slug": "usdt_trc20",
    "admin_wallet_address": "TAdminTRONaddressplaceholder123",
    "is_enabled": true,
    "min_confirmations": "19",
    "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
  }
]
```

**PUT `/{network_id}`** — update a single network. All fields optional:

```json
{
  "admin_wallet_address": "0xNewRealWalletAddress123abc",
  "is_enabled": true,
  "min_confirmations": "6",
  "name": "Ethereum",
  "symbol": "ETH",
  "contract_address": null
}
```

**What each field controls:**

| Field | Effect |
|---|---|
| `admin_wallet_address` | ⚠️ **Critical** — this is the address users send crypto to. Changes take effect on the next deposit session initiated |
| `is_enabled` | `true` = network shown to users in crypto deposit flow. `false` = hidden |
| `min_confirmations` | Minimum blockchain confirmations before deposit is considered received. String type — send as `"6"` not `6` |
| `contract_address` | ERC-20 / TRC-20 contract address for token networks (USDC, USDT). `null` for native coins |

> **`admin_wallet_address` warning:** Updating this takes effect immediately on all new deposit sessions. There is no confirmation step and no audit trail in the current implementation. Triple-check any address before saving. A typo means user funds sent to a wrong address are unrecoverable.

---

### 17.3 Banking Details Configuration

```
GET  /api/v1/admin/methods/banking
PUT  /api/v1/admin/methods/banking
```

Banking details are stored as key-value pairs in the `system_configs` table with keys prefixed `bank_`. The GET endpoint fetches all rows where `key LIKE 'bank_%'` and returns them as a flat object.

**GET** — response `data` is a dynamic key-value object:

```json
{
  "bank_bank_name": "BankApp National",
  "bank_routing_number": "021000021",
  "bank_account_number": "4892736501",
  "bank_swift_code": "BNKAUS33",
  "bank_bank_address": "123 Financial Ave, New York NY 10001",
  "bank_wire_instructions": "Include your DEP-XXXXXX reference in the memo field"
}
```

> **Note on key naming:** The GET response uses the raw database keys which have the `bank_` prefix applied twice for some fields (e.g. `bank_bank_name` instead of `bank_name`). This is because the PUT endpoint stores the key as `bank_{field_name}` where `field_name` is the request body key. When displaying these values, strip the `bank_` prefix for display purposes.

**PUT** — update any combination of fields. All optional:

```json
{
  "bank_name": "BankApp National",
  "routing_number": "021000021",
  "account_number": "4892736501",
  "swift_code": "BNKAUS33X",
  "bank_address": "456 New Ave, New York NY 10001",
  "wire_instructions": "Send wire to BankApp National. Routing: 021000021. Account: 4892736501. Reference: your DEP-XXXXXX number in memo."
}
```

- If a key already exists in `system_configs`, its value is updated.
- If it doesn't exist yet, a new row is created.
- Fields not sent are unchanged.

**How this connects to the user app:**

The `wire_instructions` stored here should be copied into the `instructions` field of the Wire Transfer deposit method (`PUT /admin/methods/deposit/{wire_method_id}`). That `instructions` field is what users see when they select wire as their deposit method. Both should be kept in sync manually until the system auto-populates it.

### 17.4 Withdrawal Methods Configuration

```
GET  /api/v1/admin/methods/withdrawal
PUT  /api/v1/admin/methods/withdrawal/{method_id}
```

> ❌ **Not implemented.** The `withdrawal_methods.py` file is empty (0 bytes). These endpoints do not exist. Withdrawal method configuration (enabling/disabling methods, setting fees, processing times) cannot be done through the admin panel at this time. This will be implemented in a future update.

---

### Phase 17 Screens to Build

- [ ] Deposit Methods list — table showing all 7 methods with toggle switches for `is_enabled` and `is_live`
- [ ] Deposit Method edit form — inline or modal, all editable fields including instructions textarea
- [ ] Crypto Networks list — table with wallet addresses, enabled toggle, min confirmations
- [ ] Crypto Network edit form — with prominent warning before saving `admin_wallet_address`
- [ ] Banking Details form — single form with all 6 fields, save button
- [ ] Wire instructions textarea (connects banking details to deposit method instructions)

---

### Key Notes for Phase 17

- **None of these endpoints are live yet** — they need router registration before they work. Build the UI now, connect when the router is updated.
- **`display_order` is a string**, not an integer — send `"1"`, `"2"`, etc.
- **`min_confirmations` is a string** — send `"3"`, `"12"`, etc.
- **Deposit method `instructions` is the text users see** in the user app. For wire and direct deposit methods, this field must contain the full banking details. Use the banking details form as the source of truth and sync manually.
- **`is_enabled: false` on a deposit method hides it from the user app immediately** — the user-side `GET /deposits/methods` reads this table directly.
- **Banking details GET response has double-prefixed keys** (`bank_bank_name`) — strip the `bank_` prefix when displaying labels in the UI.
- **No withdrawal method configuration is possible** until the file is implemented.

---

## Complete Admin API — Live Endpoint Reference

All phases combined. Use this as the quick-lookup for what you can call right now.

```
BASE: https://worldcup-orcin-chi.vercel.app/api/v1

─────────────────────────────────────────────
PHASE 14 — AUTH & DASHBOARD
─────────────────────────────────────────────
POST   /admin/auth/login              ✅ Full
POST   /admin/auth/logout             ⚠️  Returns success, no session kill
POST   /admin/auth/refresh            ⚠️  Returns success, no new tokens
POST   /admin/auth/verify-2fa         ⚠️  Returns success, no real check
GET    /admin/dashboard/stats         ✅ Full (4 fields live, 5 return null)
GET    /admin/dashboard/health        ✅ Full (no auth required)

─────────────────────────────────────────────
PHASE 15 — USER MANAGEMENT
─────────────────────────────────────────────
GET    /admin/users/list              ✅ Full — ?search= ?status= ?page= ?per_page=
GET    /admin/users/{id}              ✅ Full — all sections in one call
PUT    /admin/users/{id}/edit         ✅ Full
POST   /admin/users/{id}/suspend      ✅ Full
POST   /admin/users/{id}/activate     ✅ Full
DELETE /admin/users/{id}              ✅ Full — soft delete
PUT    /admin/users/{id}/kyc          ✅ Full — body: {status, reason}
PUT    /admin/users/{id}/limits       ✅ Full — all limit fields optional
POST   /admin/users/{id}/notes        ✅ Full — body: {note, is_pinned}
POST   /admin/users/{id}/tags         ✅ Full — body: {tag}
POST   /admin/users/{id}/balance      ✅ Full — body: {account_id, amount, reason}
POST   /admin/users/{id}/accounts     ✅ Full — creates savings account
POST   /admin/users/accounts/{id}/freeze    ✅ Full
POST   /admin/users/accounts/{id}/unfreeze  ✅ Full
POST   /admin/users/cards/{id}/freeze       ✅ Full
POST   /admin/users/cards/{id}/cancel       ✅ Full
POST   /admin/users/{id}/reset-password     ✅ Full — sets TempPass123!
POST   /admin/users/{id}/reset-2fa          ✅ Full
POST   /admin/users/{id}/force-logout       ✅ Full
POST   /admin/users/bulk              ✅ Full — body: {user_ids[], action, value}
GET    /admin/users/{id}/beneficiaries      ⚠️  Stub — returns []
GET    /admin/users/{id}/linked_accounts    ⚠️  Stub — returns []
GET    /admin/users/{id}/activity           ⚠️  Stub — returns []
GET    /admin/users/{id}/notifications      ⚠️  Stub — returns []
GET    /admin/users/{id}/support            ⚠️  Stub — returns []
GET    /admin/users/{id}/documents          ⚠️  Stub — returns []
GET    /admin/users/{id}/relationships      ⚠️  Stub — returns []
GET    /admin/users/{id}/compliance         ⚠️  Stub — returns []
GET    /admin/users/{id}/overrides          ⚠️  Stub — returns []

─────────────────────────────────────────────
PHASE 16 — TRANSACTIONS & APPROVALS
─────────────────────────────────────────────
GET    /admin/transactions/list       ✅ Full — ?type= ?status= ?user_id= ?search= ?start_date= ?end_date=
GET    /admin/transactions/{id}       ✅ Full
POST   /admin/transactions/approve    ✅ Full — body: {transaction_id, notes}
POST   /admin/transactions/reject     ✅ Full — body: {transaction_id, reason}
POST   /admin/transactions/reverse    ✅ Full — body: {transaction_id, reason}
POST   /admin/transactions/flag       ⚠️  Flag works; unflag broken
POST   /admin/transactions/bulk       ✅ Full — body: {transaction_ids[], action}
GET    /admin/transactions/export/csv ✅ Full — raw CSV, no filters, latest 5000 rows
GET    /admin/deposits/pending        ✅ Full — ?page= ?per_page=
GET    /admin/deposits/list           ✅ Full — ?status= ?page= ?per_page=
POST   /admin/deposits/{id}/approve   ✅ Full — credits balance
POST   /admin/deposits/{id}/reject    ⚠️  No reason stored, no balance restore
GET    /admin/withdrawals/pending     ✅ Full — ?page= ?per_page=
GET    /admin/withdrawals/list        ✅ Full — ?status= ?page= ?per_page=
POST   /admin/withdrawals/{id}/approve ✅ Full — debits balance
POST   /admin/withdrawals/{id}/reject  ⚠️  No balance restore (manual fix needed)

─────────────────────────────────────────────
PHASE 17 — METHOD CONFIGURATION (code written, router not updated yet)
─────────────────────────────────────────────
GET    /admin/methods/deposit         🔧 Returns 404 until router updated
PUT    /admin/methods/deposit/{id}    🔧 Returns 404 until router updated
GET    /admin/methods/crypto          🔧 Returns 404 until router updated
PUT    /admin/methods/crypto/{id}     🔧 Returns 404 until router updated
GET    /admin/methods/banking         🔧 Returns 404 until router updated
PUT    /admin/methods/banking         🔧 Returns 404 until router updated
GET    /admin/methods/withdrawal      ❌ File empty, not implemented
PUT    /admin/methods/withdrawal/{id} ❌ File empty, not implemented

─────────────────────────────────────────────
NOT YET IMPLEMENTED (all files empty)
─────────────────────────────────────────────
/admin/admins/*          ❌ Create, list, edit, delete, role assign, activity
/admin/cards/*           ❌ List all cards, freeze, cancel, replace, limits
/admin/announcements/*   ❌ Create, list, edit, delete
/admin/audit/*           ❌ List, detail, export
/admin/export/*          ❌ CSV, PDF, email, custom
/admin/fees/*            ❌ CRUD for fee schedules
/admin/interest/*        ❌ List, update interest rates
/admin/logs/*            ❌ List, detail, clear, export
/admin/notifications/*   ❌ Send, broadcast, templates
/admin/permissions/*     ❌ Assign, revoke, check
/admin/reports/*         ❌ Generate, schedule, download
/admin/roles/*           ❌ Full RBAC role management
/admin/system/*          ❌ Settings, config, maintenance
```

---

## Admin Panel Build Order

Build in this order to ship working value as fast as possible:

| # | Screen | API status |
|---|---|---|
| 1 | Login page | ✅ Live |
| 2 | Dashboard — stat cards + health badge | ✅ Live |
| 3 | Pending deposits queue + approve/reject | ✅ Live |
| 4 | Pending withdrawals queue + approve/reject | ✅ Live |
| 5 | Users list — search + status filter + pagination | ✅ Live |
| 6 | User detail — full tabbed view | ✅ Live |
| 7 | KYC approve/reject on user detail | ✅ Live |
| 8 | Balance adjust on user detail | ✅ Live |
| 9 | Suspend / activate / force logout / reset password | ✅ Live |
| 10 | Unified transactions table — filters + search | ✅ Live |
| 11 | Approve / reject / reverse from transactions table | ✅ Live |
| 12 | Deposit method config screen | 🔧 Ready when router updated |
| 13 | Crypto network config + wallet address editor | 🔧 Ready when router updated |
| 14 | Banking details form | 🔧 Ready when router updated |
| 15 | Admin management, roles, permissions | ❌ Backend not yet implemented |
| 16 | Announcements + notifications broadcast | ❌ Backend not yet implemented |
| 17 | Reports, audit logs, system settings | ❌ Backend not yet implemented |


---

## PHASE 18 — Admin Roles, Permissions & Admin Management

> Base paths:
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/roles/...`
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/permissions/...`
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/admins/...`
>
> All Phase 18 endpoints are **fully implemented and registered** — callable right now.

---

### Endpoint Status

| Endpoint | Status |
|---|---|
| `GET /admin/roles/list` | ✅ Live |
| `POST /admin/roles/create` | ✅ Live |
| `PUT /admin/roles/{role_id}` | ✅ Live |
| `DELETE /admin/roles/{role_id}` | ✅ Live — system roles protected |
| `POST /admin/roles/{role_id}/clone` | ✅ Live — copies all permissions |
| `GET /admin/roles/{role_id}/permissions` | ✅ Live |
| `PUT /admin/roles/{role_id}/permissions` | ✅ Live — replaces all permissions |
| `GET /admin/permissions/list` | ✅ Live — reads from constants |
| `GET /admin/permissions/matrix` | ✅ Live — roles × permissions grid |
| `GET /admin/permissions/check/{key}` | ⚠️ Always returns `has_permission: true` — not enforced |
| `GET /admin/admins/list` | ✅ Live |
| `POST /admin/admins/create` | ✅ Live |
| `PUT /admin/admins/{admin_id}` | ✅ Live |
| `DELETE /admin/admins/{admin_id}` | ✅ Live — super admin protected |
| `PUT /admin/admins/{admin_id}/role` | ✅ Live |
| `GET /admin/admins/activity/{admin_id}` | ✅ Live — last 50 actions |

> **Permission enforcement is not active.** The `check/{permission_key}` endpoint always returns `true` regardless of who calls it. The permission middleware exists in the codebase but is not attached to any endpoint. All authenticated (and even unauthenticated) admins can call all Phase 18 endpoints. The permission system is the data model — the enforcement layer will be added in a future update.

---

### Default Roles

Five system roles are seeded by `scripts/seed_roles.py`. System roles (`is_system: "true"`) cannot be deleted.

| Level | Name | Description |
|---|---|---|
| `1` | Super Admin | Full system access |
| `2` | Senior Admin | Can manage users and transactions |
| `3` | Admin | Can view and approve transactions |
| `4` | Support Staff | Can view users and respond to tickets |
| `5` | Viewer | Read-only access |

`level` is stored as a string (`"1"`, `"2"`, etc.). Lower number = higher access level. Level 1 (Super Admin) bypasses all permission checks once enforcement is active.

---

### All Available Permission Keys

40 permissions across 8 categories. These are the exact strings used in `ALL_PERMISSIONS` constant and stored in `admin_permissions` table.

**Users**
```
users.view          View users list
users.detail        View user details
users.edit          Edit user profile
users.suspend       Suspend/Activate users
users.delete        Delete users
users.kyc           Manage KYC approvals
users.limits        Override user limits
users.balance       Adjust user balance
users.accounts      Manage user accounts
users.cards         Manage user cards
users.security      Reset passwords/2FA
users.sessions      Force logout users
users.notes         Add internal notes
users.tags          Manage user tags
```

**Transactions**
```
transactions.view     View all transactions
transactions.approve  Approve deposits/withdrawals
transactions.reject   Reject deposits/withdrawals
transactions.reverse  Reverse transactions
transactions.flag     Flag/unflag transactions
transactions.bulk     Bulk operations
transactions.export   Export transactions
```

**Methods**
```
methods.view    View method configs
methods.edit    Edit method configs
```

**Reports**
```
reports.view    View reports
reports.export  Export reports
```

**Admin Management**
```
admins.view     View admin accounts
admins.create   Create admin accounts
admins.edit     Edit admin accounts
admins.delete   Delete admin accounts
```

**Roles & Permissions**
```
roles.view         View roles
roles.create       Create roles
roles.edit         Edit roles
roles.delete       Delete roles
permissions.assign Assign permissions
```

**Audit**
```
audit.view    View audit logs
audit.export  Export audit logs
```

**System**
```
system.settings   Manage system settings
system.templates  Manage email/SMS templates
system.legal      Manage legal documents
```

**Notifications**
```
notifications.send  Send notifications
```

---

## SECTION A — Role Management

### A1. List Roles

```
GET /api/v1/admin/roles/list
```

Returns all non-deleted roles ordered by creation date.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "name": "Super Admin",
    "description": "Full system access",
    "level": "1",
    "is_system": "true",
    "created_at": "2026-06-01T08:00:00"
  },
  {
    "id": "uuid",
    "name": "Admin",
    "description": "Can view and approve transactions",
    "level": "3",
    "is_system": "true",
    "created_at": "2026-06-01T08:00:00"
  },
  {
    "id": "uuid",
    "name": "Custom Reviewer",
    "description": "Reviews only",
    "level": "4",
    "is_system": "false",
    "created_at": "2026-06-15T10:00:00"
  }
]
```

> `is_system` is a string (`"true"` / `"false"`), not a boolean. Compare with `=== "true"` not `=== true`.

---

### A2. Create Role

```
POST /api/v1/admin/roles/create
```

Request body:
```json
{
  "name": "Compliance Officer",
  "description": "Reviews flagged transactions and KYC documents",
  "level": "3"
}
```

- `name`: 2–100 chars, required
- `description`: optional
- `level`: string — `"1"` through `"5"`. Default `"3"`. Lower = higher access.

Success response `data`:
```json
{
  "id": "uuid",
  "name": "Compliance Officer"
}
```

After creating a role, assign permissions to it via `PUT /admin/roles/{role_id}/permissions`.

---

### A3. Edit Role

```
PUT /api/v1/admin/roles/{role_id}
```

All fields optional:
```json
{
  "name": "Compliance Manager",
  "description": "Updated description",
  "level": "2"
}
```

```json
{ "success": true, "message": "Role updated" }
```

> System roles (`is_system: "true"`) can be edited — there is no protection on this. Be careful editing the name of system roles as it may affect display across the admin panel.

---

### A4. Delete Role

```
DELETE /api/v1/admin/roles/{role_id}
```

No request body. **Soft delete** — sets `is_deleted = true`.

```json
{ "success": true, "message": "Role deleted" }
```

Returns `"Cannot delete system role or not found"` if:
- The role has `is_system = "true"`, OR
- The role ID doesn't exist

> Deleting a role does not update admins currently assigned to it — their `role_id` still points to the deleted role. The admin can still log in but their permissions will resolve to empty. Show a warning before deleting a role that has admins assigned.

---

### A5. Clone Role

```
POST /api/v1/admin/roles/{role_id}/clone
```

No request body. Creates a new role named `"{original name} (Copy)"` with the same `description`, `level`, and all the same permissions copied.

Success response `data`:
```json
{
  "id": "uuid-of-new-role"
}
```

Use cloning as the starting point when creating a role similar to an existing one — clone it, then edit the name and adjust permissions.

---

### A6. Get Role Permissions

```
GET /api/v1/admin/roles/{role_id}/permissions
```

Returns a flat array of permission key strings assigned to the role:

```json
[
  "users.view",
  "users.detail",
  "transactions.view",
  "transactions.approve"
]
```

Empty array `[]` if no permissions are assigned yet.

---

### A7. Assign / Replace Role Permissions

```
PUT /api/v1/admin/roles/{role_id}/permissions
```

Request body:
```json
{
  "permissions": [
    "users.view",
    "users.detail",
    "users.kyc",
    "transactions.view",
    "transactions.approve",
    "transactions.reject"
  ]
}
```

**This is a full replace** — the endpoint marks all existing permissions as deleted and inserts the new list. Send the complete desired permission set, not just additions.

```json
{ "success": true, "message": "6 permissions assigned" }
```

> **Build a permission picker UI:** Fetch all permissions from `GET /admin/permissions/list` and render them as grouped checkboxes. Pre-check the ones from `GET /admin/roles/{role_id}/permissions`. On save, send the full checked set to this endpoint.

---

## SECTION B — Permission Reference

### B1. List All Available Permissions

```
GET /api/v1/admin/permissions/list
```

Returns all 40 defined permissions with their descriptions. This list is read from the `ALL_PERMISSIONS` constant — no DB query needed.

Success response `data` (array):
```json
[
  { "key": "users.view", "description": "View users list" },
  { "key": "users.detail", "description": "View user details" },
  { "key": "users.edit", "description": "Edit user profile" },
  { "key": "transactions.view", "description": "View all transactions" },
  { "key": "transactions.approve", "description": "Approve deposits/withdrawals" }
]
```

Use this to build the permission picker. Group by category (split on `.` — left side is the category).

---

### B2. Permission Matrix

```
GET /api/v1/admin/permissions/matrix
```

Returns a cross-reference of all roles against all permissions — which role has which permission.

Success response `data`:
```json
{
  "roles": ["Super Admin", "Senior Admin", "Admin", "Support Staff", "Viewer"],
  "permissions": ["users.view", "users.detail", "users.edit", "...all 40 keys..."],
  "matrix": {
    "Super Admin": {
      "users.view": true,
      "users.detail": true,
      "users.edit": false,
      "transactions.approve": false
    },
    "Admin": {
      "users.view": true,
      "users.detail": false,
      "transactions.approve": true
    }
  }
}
```

`matrix[role_name][permission_key]` = `true` if the role has that permission, `false` if not.

> **Build a matrix grid view:** rows = permissions, columns = roles (or vice versa). Each cell is a checkbox. On cell change, call `PUT /admin/roles/{role_id}/permissions` with the full updated set for that role. This gives a spreadsheet-style permission editor.

### B3. Check Permission (stub)

```
GET /api/v1/admin/permissions/check/{permission_key}
```

> ⚠️ **Always returns `has_permission: true`** regardless of which admin calls it or what the key is. This is a stub — permission checking is not actually enforced. Do not use this endpoint for any real access control logic.

---

## SECTION C — Admin Account Management

### C1. List Admins

```
GET /api/v1/admin/admins/list
```

Returns all non-deleted admin accounts.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "email": "admin@bankapp.com",
    "username": "superadmin",
    "full_name": "Super Admin",
    "is_active": true,
    "is_super_admin": true,
    "last_login_at": "2026-06-20T10:30:00"
  },
  {
    "id": "uuid",
    "email": "ops@bankapp.com",
    "username": "ops_admin",
    "full_name": "Operations Team",
    "is_active": true,
    "is_super_admin": false,
    "last_login_at": "2026-06-20T09:00:00"
  }
]
```

> `role_id` is not returned in the list. To show role names, maintain a local map from `GET /admin/roles/list` and match by `role_id`. A future update will join role name into the admin list response.

---

### C2. Create Admin Account

```
POST /api/v1/admin/admins/create
```

Request body:
```json
{
  "email": "newadmin@bankapp.com",
  "username": "newadmin",
  "full_name": "Jane Smith",
  "password": "SecureAdminPass1!",
  "role_id": "uuid-of-role",
  "is_super_admin": false
}
```

- `email`: valid email, required
- `username`: 3–50 chars, required
- `full_name`: required
- `password`: min 8 chars, required — hashed immediately
- `role_id`: UUID of an existing role from `GET /admin/roles/list` — required
- `is_super_admin`: bool, default `false` — only set to `true` for principals

Success response `data`:
```json
{ "id": "uuid" }
```

> No duplicate email/username check in the current implementation. Creating two admins with the same email will succeed but may cause login issues. Validate uniqueness client-side using `GET /admin/admins/list` before submitting.

---

### C3. Edit Admin

```
PUT /api/v1/admin/admins/{admin_id}
```

All fields optional:
```json
{
  "full_name": "Jane Smith-Jones",
  "is_active": false,
  "role_id": "uuid-of-new-role"
}
```

- `is_active: false` → suspends the admin — they cannot log in (login service checks `is_active`)
- `role_id` → reassigns the admin to a different role

```json
{ "success": true, "message": "Admin updated" }
```

---

### C4. Delete Admin

```
DELETE /api/v1/admin/admins/{admin_id}
```

No request body. **Soft delete** — sets `is_deleted = true`.

Returns `"Cannot delete super admin or not found"` if:
- The target admin has `is_super_admin = true`, OR
- The admin ID doesn't exist

```json
{ "success": true, "message": "Admin deleted" }
```

> Show a confirmation dialog. Super admins are permanently protected from deletion.

---

### C5. Change Admin Role

```
PUT /api/v1/admin/admins/{admin_id}/role
```

Request body:
```json
{
  "role_id": "uuid-of-new-role"
}
```

```json
{ "success": true, "message": "Role updated" }
```

Role change takes effect on the admin's **next login** — existing tokens retain the old role context until re-authentication.

---

### C6. Get Admin Activity Log

```
GET /api/v1/admin/admins/activity/{admin_id}
```

Returns the last 50 actions taken by this admin, newest first.

Success response `data` (array):
```json
[
  {
    "action": "login",
    "target_type": null,
    "target_id": null,
    "details": null,
    "ip_address": "192.168.1.1",
    "created_at": "2026-06-20T10:30:00"
  },
  {
    "action": "approve_deposit",
    "target_type": "deposit",
    "target_id": "uuid-of-deposit",
    "details": "Approved $1,000 ACH deposit",
    "ip_address": "192.168.1.1",
    "created_at": "2026-06-20T10:25:00"
  }
]
```

> Activity is only logged when the code explicitly calls `AdminActivityLog`. Currently, **only login** is logged (in `admin_service.login()`). Other actions (approve, reject, edit user, etc.) are not yet wired to log entries. The log will grow as more actions are instrumented in future updates.

---

### Phase 18 Screens to Build

**Roles section:**
- [ ] Roles list — table with name, level badge, description, system indicator, action buttons
- [ ] Create role form — name, description, level dropdown
- [ ] Edit role form — same fields, pre-filled
- [ ] Delete role confirmation dialog — with warning if admins are assigned
- [ ] Clone role button — immediately creates copy, then redirect to permission editor
- [ ] Permission editor — grouped checkboxes per category, save calls full-replace endpoint
- [ ] Permission matrix view — grid table, roles as columns, permissions as rows

**Admins section:**
- [ ] Admins list — table with name, email, role, status, last login
- [ ] Create admin form — all fields + role selector dropdown
- [ ] Edit admin form — full_name, active toggle, role selector
- [ ] Delete admin confirmation dialog
- [ ] Change role modal
- [ ] Admin activity log — per-admin table, last 50 entries

---

### Key Notes for Phase 18

- **All 16 Phase 18 endpoints are live** — fully implemented and registered. No 404s.
- **Permission enforcement is not active** — `check/{key}` always returns `true`. Do not gate any admin panel UI on this. All admins can access all pages currently.
- **`is_system` is a string** (`"true"` / `"false"`), not a boolean. Use `role.is_system === "true"` not `=== true`. Same for `is_deleted` on roles.
- **`level` is a string** — `"1"` not `1`. Lower = more access. Render level 1 as "Super Admin" and so on.
- **`PUT /{role_id}/permissions` is a full replace** — send the entire desired permission list, not just additions. If you send an empty array, all permissions are removed.
- **Role deletion does not unassign admins** — admins keep the deleted `role_id` and their permissions resolve to empty. Cross-reference admin list before allowing role deletion.
- **No duplicate check on admin creation** — validate email uniqueness client-side before calling create.
- **Admin role change takes effect on next login** — token rotation doesn't happen automatically. Inform the admin panel user that the change applies after the affected admin logs out and back in.
- **Activity log only shows login actions right now** — other admin actions (approvals, edits, etc.) are not yet instrumented. Show the log as-is with a note that full logging is in progress.
- **Super admins cannot be deleted** — the delete endpoint queries `Admin.is_super_admin == False` and returns an error if the target is a super admin. Hide the delete button for super admins in the UI.
- **Permission matrix is computed live** — it runs a DB query for every role on each call. For large role lists, this may be slow. Cache the matrix client-side and only refetch when permissions are changed.


---

## PHASE 19 — Fees, Interest Rates & Card Management

> Base paths:
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/fees/...`
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/interest/...`
> - `https://worldcup-orcin-chi.vercel.app/api/v1/admin/cards/...`
>
> All Phase 19 endpoints are **fully implemented and registered** — callable right now.

---

### Endpoint Status

| Endpoint | Status |
|---|---|
| `GET /admin/fees/list` | ✅ Live |
| `PUT /admin/fees/{fee_id}` | ✅ Live — limited fields only |
| `POST /admin/fees/create` | ✅ Live |
| `GET /admin/interest/list` | ✅ Live |
| `PUT /admin/interest/{rate_id}` | ✅ Live |
| `GET /admin/cards/all` | ✅ Live — paginated system-wide card list |
| `POST /admin/cards/issue` | ✅ Live — issues virtual card to any user |
| `POST /admin/cards/{card_id}/freeze` | ✅ Live |
| `POST /admin/cards/{card_id}/cancel` | ✅ Live |
| `PUT /admin/cards/{card_id}/limits` | ✅ Live |

> **`fee_service.py` and `interest_service.py` are both empty files.** The fee and interest endpoints work by querying the DB models directly — no service layer is used. The interest calculation task (`interest_tasks.py`) and fee application task (`fee_tasks.py`) exist in the tasks folder but their implementation status is unknown — interest accrual is not automatically applied to user accounts in the current build.

---

## SECTION A — Fee Management

### A1. List All Fees

```
GET /api/v1/admin/fees/list
```

Returns all fee schedules ordered by `category` then `name`.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "name": "Monthly Maintenance Fee",
    "slug": "monthly_maintenance",
    "amount": 0.0,
    "fee_type": "flat",
    "is_enabled": false,
    "category": "account",
    "description": "Monthly account maintenance fee"
  },
  {
    "id": "uuid",
    "name": "Domestic Wire Fee",
    "slug": "wire_domestic",
    "amount": 25.0,
    "fee_type": "flat",
    "is_enabled": true,
    "category": "transfer",
    "description": "Fee for domestic wire transfers"
  },
  {
    "id": "uuid",
    "name": "International Wire Fee",
    "slug": "wire_international",
    "amount": 35.0,
    "fee_type": "flat",
    "is_enabled": true,
    "category": "transfer",
    "description": "Fee for international wire transfers"
  }
]
```

**Fee type values:**

| `fee_type` | Meaning |
|---|---|
| `flat` | Fixed dollar amount regardless of transaction size |
| `percent` | Percentage of the transaction amount |

**Fee categories** (free-text field — these are the expected values from `scripts/seed_fees.py`):

| Category | Fee types in this group |
|---|---|
| `account` | Monthly maintenance, overdraft, returned payment |
| `transfer` | Domestic wire, international wire, ACH |
| `card` | Card payout fee, ATM out-of-network |
| `deposit` | Check deposit, cash deposit |
| `other` | Any custom fees |

> **Fees are informational only** — the `is_enabled` flag and `amount` are stored and visible to the admin but the fee application engine is not connected to transactions yet. Wire transfer fees ($25 domestic, $35 international) are still hardcoded in the transfer service, not read from this table. This table will become the live source of truth once the fee engine is completed.

---

### A2. Update Fee

```
PUT /api/v1/admin/fees/{fee_id}
```

**Only three fields can be updated** — the `UpdateFeeRequest` schema only accepts these:

```json
{
  "amount": 12.00,
  "is_enabled": true,
  "description": "Updated: $12/month for premium accounts"
}
```

- `amount`: new fee amount (float)
- `is_enabled`: `true` = fee is active, `false` = waived
- `description`: free text for admin reference

To update `name`, `slug`, `fee_type`, or `category` — use the direct DB or wait for a future update that expands this endpoint.

```json
{ "success": true, "message": "Monthly Maintenance Fee updated" }
```

---

### A3. Create New Fee

```
POST /api/v1/admin/fees/create
```

Request body:
```json
{
  "name": "Crypto Deposit Fee",
  "slug": "crypto_deposit",
  "amount": 2.50,
  "fee_type": "flat",
  "category": "deposit",
  "description": "Fee applied to crypto deposits upon approval"
}
```

Required: `name` (min 2 chars), `slug` (must be unique across all fees)
Optional: `amount` (default `0.0`), `fee_type` (default `"flat"`), `category`, `description`

`is_enabled` defaults to `true` on creation.

Success response `data`:
```json
{ "id": "uuid" }
```

> `slug` must be unique — there is no uniqueness pre-check in the endpoint, only a DB constraint. Validate uniqueness client-side by checking the existing list before creating.

---

## SECTION B — Interest Rate Management

### B1. List Interest Rates

```
GET /api/v1/admin/interest/list
```

Returns all interest rate tiers ordered by `account_type`.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "account_type": "checking",
    "rate": 0.0,
    "min_balance": 0.0,
    "max_balance": null,
    "is_enabled": false,
    "description": "Standard checking — no interest"
  },
  {
    "id": "uuid",
    "account_type": "savings",
    "rate": 0.5,
    "min_balance": 0.0,
    "max_balance": 10000.0,
    "is_enabled": true,
    "description": "Savings standard tier — 0.50% APY"
  },
  {
    "id": "uuid",
    "account_type": "savings",
    "rate": 1.0,
    "min_balance": 10000.0,
    "max_balance": null,
    "is_enabled": true,
    "description": "Savings premium tier — 1.00% APY on balances over $10,000"
  }
]
```

**Tiered rates** are supported — multiple rows for the same `account_type` with different `min_balance`/`max_balance` ranges. The interest engine applies the matching tier based on the account's current balance.

`max_balance: null` means "no upper limit" — applies to all balances above `min_balance`.

> **Interest is not currently applied automatically.** The `interest_service.py` file is empty. Rates stored here are the configured target rates — they will be applied by a scheduled task once the interest calculation engine is implemented.

### B2. Update Interest Rate

```
PUT /api/v1/admin/interest/{rate_id}
```

All fields optional:
```json
{
  "rate": 0.75,
  "min_balance": 0.0,
  "max_balance": 25000.0,
  "is_enabled": true
}
```

- `rate`: APY as a float percentage — `0.5` = 0.50%, `1.0` = 1.00%
- `min_balance`: minimum account balance for this tier to apply
- `max_balance`: maximum balance for this tier (`null` = unlimited)
- `is_enabled`: `false` disables this tier entirely

```json
{ "success": true, "message": "Rate updated" }
```

> Savings account interest rate is currently hardcoded as `0.50` in `AccountService.create_savings_account()` — it is set directly on the `Account.interest_rate` field at creation time and not read from this table. Changes here will reflect in the interest calculation engine when it is built, but do not retroactively change existing account `interest_rate` fields.

---

## SECTION C — System-Wide Card Management

These endpoints give admins direct access to all cards across all users — no `user_id` scoping needed.

### C1. List All Cards

```
GET /api/v1/admin/cards/all?page=1&per_page=20
```

All cards in the system, newest first, excluding deleted cards.

Query params: `page` (default 1), `per_page` (1–100, default 20)

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "card_type": "virtual",
      "last_four": "4521",
      "status": "active",
      "is_frozen": false,
      "created_at": "2026-06-01T08:00:00"
    },
    {
      "id": "uuid",
      "user_id": "uuid",
      "card_type": "physical",
      "last_four": "8834",
      "status": "reported_lost",
      "is_frozen": true,
      "created_at": "2026-05-15T10:00:00"
    }
  ],
  "total": 1847,
  "page": 1
}
```

Use `user_id` to link each card to the user detail page.

> `cardholder_name`, `expiry`, and `cvv` are not returned in this list — only the card management fields. Use `GET /admin/users/{user_id}` to see full card details per user.

---

### C2. Issue Card to User

```
POST /api/v1/admin/cards/issue
```

Creates a new virtual card for any user.

Request body:
```json
{
  "user_id": "uuid",
  "account_id": "uuid-of-users-checking-account",
  "cardholder_name": "JOHN DOE"
}
```

All three fields are required. Get `user_id` and `account_id` from the user detail endpoint.

Success response `data` — **returns full card details including PIN** (same as the user-side create card response):
```json
{
  "card_id": "uuid",
  "card_number": "4532819274651234",
  "expiry": "06/29",
  "cvv": "847",
  "pin": "3921",
  "last_four": "1234",
  "card_number_masked": "•••• •••• •••• 1234"
}
```

⚠️ **The full card number, CVV, and PIN are returned in this response.** Store them securely or show them once to the admin to pass to the user. This data is not retrievable again after this call.

Use this when:
- A user's card was cancelled and needs a replacement
- A new user account needs a card manually (auto-creation failed)
- Issuing a card to a user who doesn't have one

---

### C3. Freeze Card

```
POST /api/v1/admin/cards/{card_id}/freeze
```

No request body. Sets `is_frozen = true`.

```json
{ "success": true, "message": "Card frozen" }
```

No user ownership check — any `card_id` can be frozen by admin.

---

### C4. Cancel Card

```
POST /api/v1/admin/cards/{card_id}/cancel
```

No request body. Sets `status = "cancelled"` and `is_frozen = true`. Permanent.

```json
{ "success": true, "message": "Card cancelled" }
```

> Unlike the user-side cancel (Phase 15), this endpoint does **not** set `is_deleted = true` — the card record stays visible in `GET /admin/cards/all`. Cancellation is final from the user's perspective but the record persists for audit purposes.

---

### C5. Update Card Limits

```
PUT /api/v1/admin/cards/{card_id}/limits
```

All fields optional:
```json
{
  "daily_spending_limit": 10000.00,
  "per_transaction_limit": 5000.00,
  "atm_withdrawal_limit": 1000.00
}
```

Changes apply immediately — the user's card will enforce the new limits on their next transaction.

```json
{ "success": true, "message": "Card limits updated" }
```

No user ownership check — any `card_id` can be updated by admin.

---

### Phase 19 Screens to Build

**Fees section:**
- [ ] Fee schedule list — table with name, slug, amount, type, category, enabled toggle
- [ ] Edit fee inline or modal — amount, enabled toggle, description only
- [ ] Create new fee form — name, slug, amount, fee_type, category, description
- [ ] Slug uniqueness check before submit

**Interest rates section:**
- [ ] Interest rates list — grouped by account_type, showing tier ranges
- [ ] Edit rate form — rate (APY %), min_balance, max_balance, enabled toggle
- [ ] Tier visualization — show balance ranges as a stacked bar or table

**Card management section:**
- [ ] System-wide cards table — paginated, with user_id link, status badge, frozen indicator
- [ ] Issue card form — user selector + account selector + cardholder name
- [ ] Issue card result modal — show card number, CVV, PIN one time
- [ ] Freeze/cancel card buttons with confirmation dialog
- [ ] Card limits editor — three limit fields per card

---

### Key Notes for Phase 19

- **Fees are informational only** — `amount` and `is_enabled` are stored but the fee application engine is not connected to transactions. Wire fees are still hardcoded in the transfer service. Build the fee management UI now — it will go live when the engine is wired.
- **`UpdateFeeRequest` only accepts `amount`, `is_enabled`, and `description`** — you cannot change `name`, `slug`, `fee_type`, or `category` through the edit endpoint. Only the three fields.
- **Fee `slug` must be unique** — no server-side pre-check, just a DB constraint. Validate client-side.
- **Interest rates are not applied automatically** — `interest_service.py` is empty. The rates table is the configuration; the calculation engine is not yet built.
- **Savings account `interest_rate` field (0.50) is hardcoded at creation** — changes to the interest rate table do not retroactively change existing accounts' `interest_rate` column. The rate table drives future calculations only.
- **`GET /admin/interest/list` can return multiple rows for the same `account_type`** — these are tiers. Display them as a tiered table grouped by account type.
- **`rate` is APY as a float** — `0.5` means 0.50% APY. Display as `rate.toFixed(2) + "% APY"`.
- **Admin card issue returns full card details including PIN** — log this in the admin activity (manually, since auto-logging isn't wired) and treat the response as sensitive. Show once, do not store.
- **Admin card cancel does not set `is_deleted`** — unlike Phase 15's user-level cancel. Cards cancelled by admin remain visible in the system-wide list with `status: "cancelled"`.
- **No user ownership check on card freeze/cancel/limits** — any card ID works. Always source card IDs from the user detail page to ensure you're acting on the right user's card.
