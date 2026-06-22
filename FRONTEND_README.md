# Bank App Backend — Frontend Integration Guide

> Phases 1–10 complete: Authentication, User Profile, Accounts, Deposits, Withdrawals, Transfers, Bill Pay, Cards, Dashboard & Transaction History, Notifications & Alerts.
> Read this file top to bottom before writing a single line of frontend code.

---

## 1. Base URL & Interactive Docs

| Environment | Base URL |
|---|---|
| **Production (live)** | `https://worldcup-orcin-chi.vercel.app` |
| Local dev | `http://localhost:8000` |
| All API calls | `{BASE_URL}/api/v1/...` |
| Swagger UI | `{BASE_URL}/docs` |
| ReDoc | `{BASE_URL}/redoc` |
| OpenAPI JSON | `{BASE_URL}/openapi.json` |

**The backend is deployed and live.** Use `https://worldcup-orcin-chi.vercel.app` as the base URL for all development and testing.

Use the Swagger UI at `https://worldcup-orcin-chi.vercel.app/docs` to test every endpoint interactively in the browser — all endpoints are available there with request/response schemas.

---

## 2. Standard Response Envelope

**Every single endpoint** returns this wrapper — always check `success` first.

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

Validation errors (422) come from FastAPI directly:
```json
{
  "detail": [
    { "loc": ["body", "email"], "msg": "field required", "type": "value_error.missing" }
  ]
}
```

---

## 3. Authentication

### How tokens work

1. Login returns an `access_token` and `refresh_token`.
2. Send the access token on **every protected request** as a header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5...
```

3. Access token expires in **30 minutes** (configurable). Refresh it before it expires:

```
POST /api/v1/auth/refresh-token
Body: { "refresh_token": "..." }
```

4. Refresh token lives for **7 days**.

### Protected vs public endpoints

| Type | Auth required |
|---|---|
| All `/api/v1/users/*` routes | Yes — Bearer token |
| `POST /auth/signup` | No |
| `POST /auth/login` | No |
| `POST /auth/forgot-password` | No |
| `POST /auth/reset-password` | No |
| `POST /auth/forgot-username` | No |
| `POST /auth/verify-email` | No |
| `POST /auth/resend-verification` | No |
| `POST /auth/refresh-token` | No |
| `POST /auth/biometric/login` | No |
| `POST /auth/verify-2fa` | Temp token (see 2FA flow) |
| `POST /auth/verify-phone` | Yes |
| `POST /auth/2fa/enable` | Yes |
| `POST /auth/2fa/verify-setup` | Yes |
| `DELETE /auth/2fa/disable` | Yes |
| `POST /auth/biometric/enable` | Yes |
| `DELETE /auth/biometric/disable` | Yes |
| `POST /auth/logout` | Optional (provide X-Session-ID) |

### Error codes to handle globally

| HTTP Status | Meaning |
|---|---|
| 401 | Token missing, invalid, or expired — redirect to login |
| 403 | Account suspended or inactive — show account status screen |
| 422 | Validation error — show field-level errors |
| 404 | Resource not found |
| 500 | Server error |

---

## 4. PHASE 1 — Authentication Endpoints

### 4.1 Sign Up

```
POST /api/v1/auth/signup
```

**No auth required. Returns 201 on success.**

Request body:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "5551234567",
  "date_of_birth": "1990-01-15",
  "ssn": "123456789",
  "address_line1": "123 Main St",
  "address_line2": "Apt 4B",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "username": "johndoe",
  "password": "SecurePass1!",
  "confirm_password": "SecurePass1!",
  "security_question_1": "What was the name of your first pet?",
  "security_answer_1": "Fluffy",
  "security_question_2": "What city were you born in?",
  "security_answer_2": "Brooklyn",
  "agree_to_terms": true
}
```

Field rules:
- `state`: 2-letter US state code only (NY, CA, TX, etc.)
- `ssn`: 9–11 chars (accepts `123456789` or `123-45-6789`)
- `password` / `confirm_password`: 8–128 chars, must match
- `username`: 4–30 chars
- `agree_to_terms`: must be `true`
- `address_line2` is optional

Success response `data`:
```json
{
  "user_id": "uuid-here",
  "email": "john@example.com",
  "username": "johndoe",
  "message": "Account created. Please verify your email."
}
```

**After signup → redirect user to email verification screen.**

---

### 4.2 Verify Email

```
POST /api/v1/auth/verify-email
```

Request body:
```json
{
  "email": "john@example.com",
  "code": "483920"
}
```

- Code is exactly 6 digits.
- Code expires (resend if needed).

---

### 4.3 Resend Verification Code

```
POST /api/v1/auth/resend-verification
```

Request body:
```json
{
  "email": "john@example.com"
}
```

---

### 4.4 Login

```
POST /api/v1/auth/login
```

Request body:
```json
{
  "login": "johndoe",
  "password": "SecurePass1!",
  "device_name": "iPhone 15 Pro",
  "device_type": "mobile"
}
```

- `login` accepts either email OR username.
- `device_name` and `device_type` are optional but recommended for session tracking.
- `device_type` values: `mobile`, `desktop`, `tablet`.

**Normal login — success response `data`:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800,
  "requires_2fa": false,
  "session_id": "uuid-here"
}
```

**2FA login — success response `data`:**
```json
{
  "access_token": "eyJ...(temp token)...",
  "requires_2fa": true,
  "session_id": "uuid-here"
}
```

When `requires_2fa` is `true`:
- Store the temp token temporarily.
- Show the 2FA code entry screen.
- Send the temp token as `Authorization: Bearer <temp_token>` to `/auth/verify-2fa`.

**Failed login errors (in `message` field):**
- `"Invalid credentials"`
- `"Account is locked. Try again in X minutes."`
- `"Account is suspended"`

Store `session_id` from the response — used for logout.

---

### 4.5 Verify 2FA (complete login)

```
POST /api/v1/auth/verify-2fa
Authorization: Bearer <temp_token_from_login>
```

Request body:
```json
{
  "code": "123456",
  "trust_device": true,
  "device_name": "iPhone 15 Pro",
  "device_type": "mobile"
}
```

Success response `data`:
```json
{
  "access_token": "eyJ...(real token)...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800,
  "trusted_device_id": "uuid-or-null"
}
```

---

### 4.6 Logout

```
POST /api/v1/auth/logout
X-Session-ID: <session_id_from_login>
```

No request body needed. Pass `X-Session-ID` header with the session ID from login.

---

### 4.7 Refresh Token

```
POST /api/v1/auth/refresh-token
```

Request body:
```json
{
  "refresh_token": "eyJ..."
}
```

Success response `data`:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### 4.8 Forgot Password

```
POST /api/v1/auth/forgot-password
```

Request body:
```json
{
  "email": "john@example.com"
}
```

Always returns `success: true` regardless of whether the email exists (security measure). Show a generic success message.

---

### 4.9 Reset Password

```
POST /api/v1/auth/reset-password
```

Request body:
```json
{
  "token": "token-from-email-link",
  "new_password": "NewSecurePass1!",
  "confirm_password": "NewSecurePass1!"
}
```

The reset token comes from the link in the password reset email (e.g. `?token=abc123`).

---

### 4.10 Forgot Username

```
POST /api/v1/auth/forgot-username
```

Request body:
```json
{
  "email": "john@example.com"
}
```

Sends an email with the username. Always returns success.

---

### 4.11 Verify Phone

```
POST /api/v1/auth/verify-phone
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "code": "839201"
}
```

Code is 6 digits, sent via SMS.

---

### 4.12 Setup 2FA (enable)

```
POST /api/v1/auth/2fa/enable
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "method": "authenticator",
  "phone_number": null
}
```

- `method`: `"authenticator"`, `"sms"`, or `"email"`
- `phone_number`: required only if method is `"sms"`

Success response `data`:
```json
{
  "secret": "BASE32SECRET",
  "qr_code_url": "otpauth://totp/BankApp:john@example.com?secret=...",
  "manual_key": "BASE32SECRET",
  "message": "Scan the QR code with your authenticator app"
}
```

Display the `qr_code_url` as a QR code image (use a QR library). Show `manual_key` as fallback for manual entry.

---

### 4.13 Verify 2FA Setup

```
POST /api/v1/auth/2fa/verify-setup
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "code": "123456"
}
```

User enters the 6-digit code from their authenticator app to confirm setup.

---

### 4.14 Disable 2FA

```
DELETE /api/v1/auth/2fa/disable
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "code": "123456",
  "password": "SecurePass1!"
}
```

---

### 4.15 Enable Biometric Login

```
POST /api/v1/auth/biometric/enable
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "biometric_token": "device-generated-unique-token",
  "device_name": "iPhone 15 Pro",
  "device_type": "mobile"
}
```

The `biometric_token` is generated by the mobile device's biometric framework (Face ID / Touch ID). Store the token locally on the device and send it here once.

---

### 4.16 Biometric Login

```
POST /api/v1/auth/biometric/login
```

Request body:
```json
{
  "biometric_token": "device-generated-unique-token"
}
```

Returns same token response as normal login.

---

### 4.17 Disable Biometric

```
DELETE /api/v1/auth/biometric/disable
Authorization: Bearer <access_token>
```

No request body.

---

## 5. PHASE 2 — User Profile & Account Management

All endpoints below require `Authorization: Bearer <access_token>`.

---

### 5.1 Get Profile

```
GET /api/v1/users/profile
```

Response `data`:
```json
{
  "id": "uuid",
  "email": "john@example.com",
  "username": "johndoe",
  "phone": "5551234567",
  "is_email_verified": true,
  "is_phone_verified": false,
  "is_2fa_enabled": false,
  "biometric_enabled": false,
  "kyc_status": "not_submitted",
  "is_active": true,
  "last_login_at": "2026-06-20T10:30:00",
  "created_at": "2026-06-01T08:00:00",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "ssn_last_four": "6789",
  "address_line1": "123 Main St",
  "address_line2": "Apt 4B",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "profile_picture_url": null,
  "occupation": "Software Engineer",
  "employer": "Acme Corp"
}
```

`kyc_status` values: `not_submitted`, `pending`, `verified`, `rejected`

---

### 5.2 Update Profile

```
PUT /api/v1/users/profile
```

All fields are optional — send only what changed:
```json
{
  "first_name": "Johnny",
  "last_name": "Doe",
  "phone": "5559876543",
  "address_line1": "456 Elm St",
  "address_line2": null,
  "city": "Brooklyn",
  "state": "NY",
  "zip_code": "11201",
  "occupation": "Lead Engineer",
  "employer": "New Corp"
}
```

Returns the updated full profile in `data`.

---

### 5.3 Change Password

```
PUT /api/v1/users/password
```

```json
{
  "current_password": "OldPass1!",
  "new_password": "NewPass2!",
  "confirm_password": "NewPass2!"
}
```

---

### 5.4 Change PIN

```
PUT /api/v1/users/pin
```

```json
{
  "current_pin": "1234",
  "new_pin": "5678"
}
```

- PIN is 4–6 digits.
- `current_pin` can be omitted if user never set one.

---

### 5.5 Security Questions

Get (answers are always masked — only questions are returned):
```
GET /api/v1/users/security-questions
```

Response `data`:
```json
[
  { "id": "uuid", "question_number": 1, "question": "What was your first pet's name?" },
  { "id": "uuid", "question_number": 2, "question": "What city were you born in?" }
]
```

Update (requires password confirmation):
```
PUT /api/v1/users/security-questions
```

```json
{
  "password": "SecurePass1!",
  "question_1": "What was the name of your first school?",
  "answer_1": "Lincoln Elementary",
  "question_2": "What is your mother's maiden name?",
  "answer_2": "Smith"
}
```

---

### 5.6 KYC Status

```
GET /api/v1/users/kyc/status
```

Response `data`:
```json
{
  "status": "not_submitted"
}
```

Status values: `not_submitted` → `pending` → `verified` | `rejected`

---

### 5.7 Upload KYC Document

```
POST /api/v1/users/documents/upload
Content-Type: multipart/form-data
```

Form fields:
- `document_type` (string): `driver_license`, `passport`, `selfie`, `proof_of_address`
- `file` (binary): the document image/PDF

```javascript
const formData = new FormData();
formData.append('document_type', 'driver_license');
formData.append('file', fileObject);

fetch('/api/v1/users/documents/upload', {
  method: 'POST',
  headers: { 'Authorization': 'Bearer ' + token },
  body: formData,
});
```

Response `data`:
```json
{
  "id": "uuid",
  "document_type": "driver_license",
  "verification_status": "pending"
}
```

---

### 5.8 Get KYC Documents

```
GET /api/v1/users/documents
```

Response `data` (array):
```json
[
  {
    "id": "uuid",
    "document_type": "driver_license",
    "file_url": "/uploads/abc.jpg",
    "file_name": "license.jpg",
    "verification_status": "pending",
    "rejection_reason": null,
    "created_at": "2026-06-15T12:00:00"
  }
]
```

`verification_status` values: `pending`, `approved`, `rejected`

---

### 5.9 Beneficiaries

**List:**
```
GET /api/v1/users/beneficiaries
```

**Add:**
```
POST /api/v1/users/beneficiaries
```

```json
{
  "name": "Jane Doe",
  "account_number": "1234567890",
  "routing_number": "021000021",
  "bank_name": "Chase Bank",
  "email": "jane@example.com",
  "phone": "5552345678",
  "relationship": "Family",
  "nickname": "Mom"
}
```

Required: `name`, `account_number`. All others optional.

**Update:**
```
PUT /api/v1/users/beneficiaries/{beneficiary_id}
```

Same fields as add, all optional.

**Delete:**
```
DELETE /api/v1/users/beneficiaries/{beneficiary_id}
```

Beneficiary response object:
```json
{
  "id": "uuid",
  "name": "Jane Doe",
  "account_number": "1234567890",
  "routing_number": "021000021",
  "bank_name": "Chase Bank",
  "email": "jane@example.com",
  "phone": "5552345678",
  "relationship": "Family",
  "nickname": "Mom",
  "created_at": "2026-06-10T09:00:00"
}
```

---

### 5.10 Linked External Bank Accounts

**List:**
```
GET /api/v1/users/linked-accounts
```

Note: `account_number` is masked as `****1234` in the response.

**Add:**
```
POST /api/v1/users/linked-accounts
```

```json
{
  "bank_name": "Chase Bank",
  "account_number": "9876543210",
  "routing_number": "021000021",
  "account_type": "checking"
}
```

`account_type`: `checking` or `savings` (default: `checking`)

Response `data`:
```json
{
  "id": "uuid",
  "micro_deposits_note": "Two small deposits have been sent. Enter the amounts to verify."
}
```

After adding, the backend simulates two micro-deposits. User must verify them.

**Verify with micro-deposits:**
```
POST /api/v1/users/linked-accounts/{account_id}/verify
```

```json
{
  "amount_1": 0.32,
  "amount_2": 0.67
}
```

> **Dev note:** During development, if verification fails the response `data` includes a `hint` field with the expected amounts. Remove this hint display from production UI.

**Remove:**
```
DELETE /api/v1/users/linked-accounts/{account_id}
```

---

### 5.11 Account Limits

```
GET /api/v1/users/limits
```

Response `data`:
```json
{
  "daily_deposit_limit": 10000.0,
  "daily_withdrawal_limit": 5000.0,
  "daily_transfer_limit": 10000.0,
  "per_transaction_limit": 5000.0,
  "monthly_deposit_limit": 50000.0,
  "monthly_withdrawal_limit": 25000.0,
  "card_spending_limit": 5000.0,
  "atm_withdrawal_limit": 500.0
}
```

All amounts are in USD.

---

### 5.12 Notification Preferences

**Get:**
```
GET /api/v1/users/notifications/preferences
```

**Update (send only fields to change):**
```
PUT /api/v1/users/notifications/preferences
```

```json
{
  "push_enabled": true,
  "push_deposits": true,
  "push_withdrawals": true,
  "push_transfers": true,
  "push_security": true,
  "email_enabled": true,
  "email_deposits": true,
  "email_withdrawals": false,
  "email_transfers": true,
  "email_security": true,
  "email_statements": true,
  "sms_enabled": false,
  "sms_deposits": false,
  "sms_withdrawals": false,
  "sms_security": true
}
```

All fields are optional booleans.

---

### 5.13 App Preferences

**Get:**
```
GET /api/v1/users/preferences
```

**Update:**
```
PUT /api/v1/users/preferences
```

```json
{
  "language": "en",
  "theme": "dark",
  "currency_display": "USD",
  "timezone": "America/New_York"
}
```

> Note: These preferences are currently a placeholder — the backend does not persist them. Store them in the client (AsyncStorage / localStorage) and send them here for future server sync.

---

### 5.14 Active Sessions

**List:**
```
GET /api/v1/users/sessions
```

Response `data` (array):
```json
[
  {
    "id": "uuid",
    "ip_address": "192.168.1.1",
    "device_name": "iPhone 15 Pro",
    "device_type": "mobile",
    "location": "New York, US",
    "is_active": true,
    "created_at": "2026-06-20T10:00:00",
    "expires_at": "2026-06-27T10:00:00"
  }
]
```

**Revoke a session (force logout from that device):**
```
DELETE /api/v1/users/sessions/{session_id}
```

---

### 5.15 Trusted Devices

**List:**
```
GET /api/v1/users/devices
```

Response `data` (array):
```json
[
  {
    "id": "uuid",
    "device_name": "iPhone 15 Pro",
    "device_type": "mobile",
    "is_trusted": true,
    "last_used_at": "2026-06-20T10:00:00",
    "created_at": "2026-06-01T08:00:00"
  }
]
```

**Remove device trust:**
```
DELETE /api/v1/users/devices/{device_id}
```

---

### 5.16 Activity Log

```
GET /api/v1/users/activity?page=1&per_page=50
```

Query params:
- `page`: integer ≥ 1, default 1
- `per_page`: integer 1–100, default 50

Response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "action": "login",
      "description": "Login from New York, US",
      "ip_address": "192.168.1.1",
      "created_at": "2026-06-20T10:00:00"
    }
  ],
  "page": 1,
  "per_page": 50,
  "total": 142
}
```

---

### 5.17 Close Account

```
POST /api/v1/users/close-account
```

```json
{
  "reason": "I no longer need this account",
  "destination_account": "ACC-12345",
  "confirm": true
}
```

- `confirm` must be `true` or the request is rejected.
- `destination_account` is optional — for specifying where remaining balance should be sent.

---

## 6. Complete Auth Flow Diagrams

### Normal Sign-up → Login Flow

```
1. POST /auth/signup
        ↓
2. Show "Check your email" screen
        ↓
3. POST /auth/verify-email  (user enters 6-digit code)
        ↓
4. POST /auth/login
        ↓ (requires_2fa: false)
5. Store access_token + refresh_token + session_id
        ↓
6. All protected API calls use: Authorization: Bearer <access_token>
```

### 2FA Login Flow

```
1. POST /auth/login
        ↓ (requires_2fa: true, access_token is a TEMP token)
2. Show 2FA code entry screen
        ↓
3. POST /auth/verify-2fa
   Authorization: Bearer <temp_token>
        ↓
4. Receive real access_token + refresh_token
        ↓
5. Continue as normal
```

### Token Refresh Flow

```
When you get a 401 "Invalid or expired token":
1. POST /auth/refresh-token  { "refresh_token": "..." }
        ↓ (success)
2. Store new access_token + refresh_token
3. Retry the original request
        ↓ (refresh also fails with 401)
4. Token fully expired — redirect to login
```

---

## 7. Key Field Notes & Validation

| Field | Rule |
|---|---|
| `state` | 2-letter US code: NY, CA, TX, etc. |
| `ssn` | 9–11 chars, digits only or with dashes |
| `password` | 8–128 chars, must match `confirm_password` |
| `pin` | 4–6 digits |
| `code` (OTP / 2FA) | Exactly 6 digits |
| `username` | 4–30 chars |
| `routing_number` | 9-digit US routing number |
| `account_type` | `"checking"` or `"savings"` |
| `device_type` | `"mobile"`, `"desktop"`, `"tablet"` |
| `2fa method` | `"authenticator"`, `"sms"`, `"email"` |
| `kyc_status` | `not_submitted`, `pending`, `verified`, `rejected` |

---

## 8. Screens to Build (Phases 1 & 2)

### Auth Screens
- [ ] Sign Up (multi-step form recommended)
- [ ] Email Verification (enter 6-digit code)
- [ ] Login (email/username + password)
- [ ] 2FA Code Entry
- [ ] Forgot Password (enter email)
- [ ] Reset Password (enter new password from link)
- [ ] Forgot Username (enter email)
- [ ] Biometric Login (device biometric trigger)

### Profile & Settings Screens
- [ ] Profile View
- [ ] Edit Profile
- [ ] Change Password
- [ ] Change PIN
- [ ] Security Questions (view & update)
- [ ] KYC Status page
- [ ] KYC Document Upload
- [ ] 2FA Setup (QR code display + code confirm)
- [ ] Biometric Setup
- [ ] Notification Preferences
- [ ] App Preferences (theme, language, timezone)
- [ ] Active Sessions List
- [ ] Trusted Devices List
- [ ] Activity Log (paginated)
- [ ] Beneficiaries List, Add, Edit, Delete
- [ ] Linked Accounts List, Add, Verify, Remove
- [ ] Account Limits View
- [ ] Close Account (confirmation flow)

---

## 9. Dev / Testing Helpers

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/auth/test-verification-code?email=...` | Get verification code directly (dev only — remove from prod) |
| `GET /docs` | Interactive Swagger UI for all endpoints |
| `GET /redoc` | Full API documentation |

For linked account micro-deposit verification in development, the verify response includes a `hint` with the expected amounts if the submitted amounts are wrong.

---

## 10. What's Coming Next (Phases 3+)

The backend will be adding:
- **Bank accounts** (checking, savings — balances, statements)
- **Transactions** (deposits, withdrawals, transfers, history)
- **Cards** (debit card management, freeze/unfreeze, limits)
- **Admin panel** (already scaffolded)
- **Alerts** (balance, transaction, security alerts)

Design your state management and routing with these upcoming modules in mind.


---

# PHASE 3 — Accounts & Balances

> All endpoints require `Authorization: Bearer <access_token>`.
> Base path: `/api/v1/accounts/...`

---

## 11. Account Object

Every account endpoint returns account objects in this shape:

```json
{
  "id": "uuid",
  "account_number": "4820193847261",
  "account_type": "checking",
  "account_name": "Primary Checking",
  "balance": 2540.00,
  "available_balance": 2340.00,
  "pending_balance": 200.00,
  "currency": "USD",
  "is_active": true,
  "is_frozen": false,
  "interest_rate": 0.0,
  "overdraft_protection": false,
  "created_at": "2026-06-01T08:00:00"
}
```

### Balance fields explained

| Field | Meaning |
|---|---|
| `balance` | Actual current balance (posted transactions only) |
| `available_balance` | What the user can spend right now (`balance` minus any pending holds) |
| `pending_balance` | Amount held/pending — not yet settled |

Always show `available_balance` as the primary number on dashboards. Show `pending_balance` as a secondary line if it is greater than 0.

### Account type values

| Value | Description |
|---|---|
| `checking` | Primary checking account — auto-created on signup |
| `savings` | Savings account — user-created, earns interest |

### Account status flags

| Flag | When true |
|---|---|
| `is_active: false` | Account is closed or deactivated |
| `is_frozen: true` | Account is temporarily frozen (admin action) — show a frozen banner, block transactions |

---

## 12. Checking Account Endpoints

### 12.1 Get Checking Account

```
GET /api/v1/accounts/checking
```

Returns the user's primary checking account.

Success response `data`:
```json
{
  "id": "uuid",
  "account_number": "4820193847261",
  "account_type": "checking",
  "account_name": "Primary Checking",
  "balance": 2540.00,
  "available_balance": 2340.00,
  "pending_balance": 200.00,
  "currency": "USD",
  "is_active": true,
  "is_frozen": false,
  "interest_rate": 0.0,
  "overdraft_protection": false,
  "created_at": "2026-06-01T08:00:00"
}
```

If no checking account exists (should not happen for active users — it is auto-created on signup):
```json
{ "success": false, "message": "No checking account found" }
```

> **Note:** The checking account is created automatically when the user signs up. You never need to call a "create checking" endpoint — just fetch it on login.

---

## 13. Savings Account Endpoints

### 13.1 Create Savings Account

```
POST /api/v1/accounts/savings
```

Status: **201 Created**

Request body:
```json
{
  "account_name": "Emergency Fund",
  "initial_deposit": 500.00
}
```

- `account_name`: optional, max 100 chars. Defaults to `"Savings Account"`.
- `initial_deposit`: optional float ≥ 0. Defaults to `0.0`. If greater than 0, funds are pulled from the checking account. If checking has insufficient available balance, the account is still created but with a $0 balance.

Success response `data`:
```json
{
  "id": "uuid",
  "account_number": "5931820473652",
  "account_type": "savings",
  "balance": 500.00
}
```

### 13.2 Get Savings Accounts

```
GET /api/v1/accounts/savings
```

Returns an **array** of all savings accounts (a user can have multiple).

Success response `data`:
```json
[
  {
    "id": "uuid",
    "account_number": "5931820473652",
    "account_type": "savings",
    "account_name": "Emergency Fund",
    "balance": 500.00,
    "available_balance": 500.00,
    "pending_balance": 0.0,
    "currency": "USD",
    "is_active": true,
    "is_frozen": false,
    "interest_rate": 0.5,
    "overdraft_protection": false,
    "created_at": "2026-06-10T09:00:00"
  }
]
```

Returns an empty array `[]` if no savings accounts exist yet.

> **Note:** Savings accounts earn **0.50% APY** interest by default (`interest_rate: 0.5`). Display this on the savings account card.

---

## 14. Balance Endpoints

### 14.1 Get All Balances (Dashboard)

```
GET /api/v1/accounts/balances
```

The main endpoint for a dashboard overview. Returns all accounts plus a combined total.

Success response `data`:
```json
{
  "accounts": [
    {
      "id": "uuid-checking",
      "account_number": "4820193847261",
      "account_type": "checking",
      "account_name": "Primary Checking",
      "balance": 2540.00,
      "available_balance": 2340.00,
      "pending_balance": 200.00,
      "currency": "USD",
      "is_active": true,
      "is_frozen": false,
      "interest_rate": 0.0,
      "overdraft_protection": false,
      "created_at": "2026-06-01T08:00:00"
    },
    {
      "id": "uuid-savings",
      "account_number": "5931820473652",
      "account_type": "savings",
      "account_name": "Emergency Fund",
      "balance": 500.00,
      "available_balance": 500.00,
      "pending_balance": 0.0,
      "currency": "USD",
      "is_active": true,
      "is_frozen": false,
      "interest_rate": 0.5,
      "overdraft_protection": false,
      "created_at": "2026-06-10T09:00:00"
    }
  ],
  "total_balance": 3040.00
}
```

`total_balance` is the sum of all account `balance` fields.

### 14.2 Get Single Account Balance

```
GET /api/v1/accounts/{account_id}/balance
```

Returns full detail for one account by its `id` (UUID).

Success response `data` — same shape as a single account object.

Returns 404 if the account doesn't exist or doesn't belong to the current user.

---

## 15. Statement Endpoints

### 15.1 Get Statements for an Account

```
GET /api/v1/accounts/{account_id}/statements
```

Returns a list of monthly statements for the given account.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "statement_date": "2026-06-30",
    "period_start": "2026-06-01",
    "period_end": "2026-06-30",
    "opening_balance": 1200.00,
    "closing_balance": 2540.00,
    "total_deposits": 3000.00,
    "total_withdrawals": 660.00,
    "total_fees": 0.00,
    "interest_earned": 0.00,
    "file_url": "/uploads/statements/stmt-uuid.pdf"
  }
]
```

Returns an empty array `[]` if no statements have been generated yet.

`file_url` can be `null` if the PDF has not been generated. Check before rendering a download link.

### 15.2 Generate Statement

```
POST /api/v1/accounts/{account_id}/statements/generate
```

Triggers generation of a new monthly statement for the account.

No request body needed.

Success response `data`:
```json
{
  "id": "uuid",
  "statement_date": "2026-06-30"
}
```

After generating, call `GET /{account_id}/statements` again to get the full details.

Returns 404 if the account is not found or doesn't belong to the current user.

---

## 16. Recommended Account Data Flow

### On app load / login

```
1. GET /api/v1/accounts/balances
   → Store all accounts + total_balance in global state
   → Use total_balance on home screen hero section
   → Use individual accounts for account cards

2. GET /api/v1/accounts/checking
   → Use for the primary checking card detail screen
```

### On savings screen load

```
1. GET /api/v1/accounts/savings
   → Render each savings account as a card
   → If empty array, show "Create Savings Account" CTA
```

### On account detail screen

```
1. GET /api/v1/accounts/{account_id}/balance
   → Show balance breakdown (current / available / pending)

2. GET /api/v1/accounts/{account_id}/statements
   → Show statements list below balance
```

---

## 17. Phase 3 Screens to Build

- [ ] Dashboard / Home — total balance hero + account cards
- [ ] Checking Account Detail — balance breakdown, frozen state banner
- [ ] Savings Accounts List — with "Create Savings" button
- [ ] Create Savings Account — form (name + optional initial deposit amount)
- [ ] Account Detail — balance breakdown for any account by ID
- [ ] Statements List — per account, with download link if `file_url` is set
- [ ] Generate Statement — button that triggers generation, then reloads list

---

## 18. Key Notes for Phase 3

- **Checking account always exists** after signup. Never show a "no account" empty state for checking unless the account is suspended/frozen.
- **Savings accounts are optional and user-created.** A user might have zero savings accounts.
- **Multiple savings accounts are supported.** Always render a list, not a single item.
- **`available_balance` is the spendable amount** — use it for transaction validation on the frontend (e.g., disabling a "Transfer" button if the amount exceeds `available_balance`).
- **`pending_balance > 0`** means there are uncleared transactions. Show a tooltip or info icon explaining what pending means.
- **`is_frozen: true`** — block all transaction initiation from that account on the frontend. Show a clear message.
- **`interest_rate`** on savings is `0.5` (meaning 0.50% APY). Display as `0.50% APY` in the UI.
- **Statement `file_url`** may be a relative path (`/uploads/...`) — prepend `BASE_URL` before using it as a download link.


---

# PHASE 4 — Deposits (All Methods)

> All deposit endpoints require `Authorization: Bearer <access_token>` unless stated otherwise.
> Base path: `/api/v1/deposits/...`

---

## 19. Deposit Concepts

### Deposit status values

Every deposit record has a `status` field. These are the possible values:

| Status | Meaning | What to show |
|---|---|---|
| `pending` | Submitted, waiting for admin review | "Pending" badge (yellow) |
| `approved` | Admin approved, funds credited | "Completed" badge (green) |
| `rejected` | Admin rejected the deposit | "Rejected" badge (red) + show `admin_notes` |
| `cancelled` | Cancelled before processing | "Cancelled" badge (grey) |

**All deposit methods start in `pending` status.** Funds are not available until an admin approves. Show users a clear message that deposits are under review.

### Deposit response object

Every deposit method returns this base object on success:

```json
{
  "reference": "DEP-A3F92K",
  "deposit_id": "uuid",
  "amount": 500.00,
  "fee": 0.00,
  "net_amount": 500.00,
  "status": "pending"
}
```

- `reference` — unique deposit reference code. Display this to the user as a tracking number.
- `fee` — currently `0.0` for all methods.
- `net_amount` — `amount - fee`. This is what gets credited when approved.

### Selecting a target account

All non-crypto deposit endpoints accept an optional `account_id` field. If omitted, the backend defaults to the user's first account (checking). It is best practice to always send `account_id` explicitly so the user knows exactly which account receives the funds.

---

## 20. Get Deposit Methods

```
GET /api/v1/deposits/methods
```

**No auth required.**

Returns all available deposit methods from the database. Use this to dynamically render the deposit method selection screen — do not hardcode the list.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "name": "Crypto",
    "slug": "crypto",
    "description": "Deposit using Bitcoin, Ethereum, USDC, or USDT",
    "is_enabled": true,
    "min_amount": 0.01,
    "max_amount": 1000000.0,
    "fee_type": "flat",
    "fee_amount": 0.0,
    "processing_time": "1-3 business days",
    "instructions": "...",
    "icon": "bitcoin"
  },
  {
    "id": "uuid",
    "name": "ACH Transfer",
    "slug": "ach",
    "description": "Transfer from your bank account via ACH",
    "is_enabled": true,
    "min_amount": 1.0,
    "max_amount": 10000.0,
    "fee_type": "flat",
    "fee_amount": 0.0,
    "processing_time": "2-3 business days",
    "instructions": null,
    "icon": "bank"
  }
]
```

The 7 method slugs are: `crypto`, `ach`, `wire`, `check`, `cash`, `direct_deposit`, `p2p`.

Only render methods where `is_enabled: true`. Use `slug` to route to the correct deposit form. Use `min_amount` / `max_amount` for frontend validation before submitting.

---

## 21. Crypto Deposit

Crypto is the only "real" deposit method — it creates an actual blockchain deposit session with a wallet address and QR code. Admin manually approves after seeing the on-chain transaction.

### 21.1 Get Supported Crypto Networks

Before showing the crypto deposit form, fetch the supported networks:

```
GET /api/v1/deposits/crypto/networks
```

> ⚠️ If this endpoint is not yet exposed as a standalone route, use the `methods` endpoint and filter by `slug: "crypto"`, then hardcode the 4 networks below from the constants. The backend will expose a dedicated networks endpoint in a future update.

Supported networks (hardcoded constants for now):

| Name | Symbol | Slug | Network Type |
|---|---|---|---|
| Bitcoin | BTC | `btc` | bitcoin |
| Ethereum | ETH | `eth` | ethereum |
| USD Coin | USDC | `usdc_erc20` | ERC-20 |
| Tether USD | USDT | `usdt_trc20` | TRC-20 |

### 21.2 Initiate Crypto Deposit

```
POST /api/v1/deposits/crypto/initiate
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 250.00,
  "network": "eth"
}
```

- `amount`: float > 0 — the USD value the user wants to deposit
- `network`: one of `btc`, `eth`, `usdc_erc20`, `usdt_trc20`

Success response `data`:
```json
{
  "session_id": "uuid",
  "reference": "DEP-X7K2M9",
  "address": "0x742d35Cc6634C0539085a3c1E39c7f5eC5D8d9a1",
  "network": "eth",
  "expected_amount": 250.00,
  "qr_code": "data:image/png;base64,iVBORw0KGgo...",
  "deep_link": "ethereum:0x742d35Cc6634C0539085a3c1E39c7f5eC5D8d9a1?value=250",
  "expires_at": "2026-06-22T10:30:00"
}
```

**How to use each field:**

| Field | Usage |
|---|---|
| `address` | Display as the "Send to this address" value with a copy button |
| `qr_code` | Base64 PNG — render directly in an `<img>` tag: `src="data:image/png;base64,..."` |
| `deep_link` | "Open Wallet App" button — use as a URL/href to launch the user's crypto wallet app |
| `reference` | Show as tracking reference. User must include this in their wallet memo/note if possible |
| `expires_at` | Show a countdown timer. Session expires after 24 hours |
| `expected_amount` | Show as the amount to send |

### 21.3 Poll Deposit Session Status

After the user sends crypto, they can check the status of their session:

```
GET /api/v1/deposits/crypto/session/{reference}
Authorization: Bearer <access_token>
```

Response `data`:
```json
{
  "reference": "DEP-X7K2M9",
  "status": "pending",
  "network": "eth",
  "admin_address": "0x742d35Cc6634C0539085a3c1E39c7f5eC5D8d9a1"
}
```

Session status values: `pending`, `confirmed`, `expired`, `failed`

Poll this endpoint every 30–60 seconds after the user says they've sent the crypto, and update the UI accordingly. Once `status` is `confirmed`, show a success state and direct to deposit history.

### 21.4 Crypto Deposit UX Flow

```
1. User selects "Crypto" deposit method
2. User selects network (BTC / ETH / USDC / USDT)
3. User enters USD amount
4. POST /deposits/crypto/initiate
        ↓
5. Show deposit screen:
   - Wallet address (with copy button)
   - QR code image
   - "Open Wallet App" button (deep_link)
   - Amount to send
   - Reference number
   - Expiry countdown timer
        ↓
6. User sends crypto from their own wallet
7. User taps "I've sent it" → start polling
8. GET /deposits/crypto/session/{reference}  every 30s
        ↓ status = confirmed
9. Show success screen
        ↓ status = expired
9. Show "Session expired" → offer to start again
```

---

## 22. ACH Transfer Deposit

```
POST /api/v1/deposits/ach
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 1000.00,
  "account_id": "uuid-of-target-account",
  "notes": "Payroll transfer"
}
```

- `amount`: float > 0
- `account_id`: optional — which bank account to deposit into. Defaults to checking if omitted.
- `notes`: optional free-text note

Success response `data`:
```json
{
  "reference": "DEP-B8L3N1",
  "deposit_id": "uuid",
  "amount": 1000.00,
  "fee": 0.00,
  "net_amount": 1000.00,
  "status": "pending"
}
```

Show the user their reference number and a message that ACH transfers take 2–3 business days to process.

---

## 23. Wire Transfer Deposit

```
POST /api/v1/deposits/wire
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 5000.00,
  "account_id": "uuid-of-target-account",
  "notes": "Investment wire from Chase"
}
```

Success response `data`: same base deposit object (reference, deposit_id, amount, fee, net_amount, status).

**Before the user submits**, display the bank's wire receiving instructions. These come from `GET /api/v1/deposits/methods` — find the method with `slug: "wire"` and display its `instructions` field. The instructions contain the bank name, routing number, and account number the user needs to wire to.

---

## 24. Mobile Check Deposit

```
POST /api/v1/deposits/check
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 350.00,
  "account_id": "uuid-of-target-account",
  "notes": "Tax refund check"
}
```

Success response `data`: same base deposit object.

> **Note on check images:** The current backend accepts the amount and notes only — it does not yet process the actual check image file. The frontend can capture front/back check photos using the camera (for future integration), but for now only submit the `amount` field. Tell the user their check will be reviewed within 2 business days.

---

## 25. Cash Deposit

```
POST /api/v1/deposits/cash
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 200.00,
  "account_id": "uuid-of-target-account",
  "notes": "Cash at CVS location"
}
```

Success response `data`: same base deposit object.

> **Cash locations:** The backend does not yet serve a live ATM/partner location list. For now, display a static list of partner networks (Green Dot, MoneyGram, Walmart, CVS) on the cash deposit screen with a note to "Show your reference number to the cashier." A live location finder endpoint will be added in a future phase.

---

## 26. Direct Deposit Setup

```
POST /api/v1/deposits/direct_deposit
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 2500.00,
  "account_id": "uuid-of-target-account",
  "notes": "Biweekly payroll - ACME Corp"
}
```

Success response `data`: same base deposit object.

**Direct deposit info screen:** Before submitting, display the user's banking details they need to give their employer:
- Bank routing number: fetched from `GET /api/v1/accounts/checking` → use the `account_number` to look up routing info (routing number is not currently returned directly — display a hardcoded routing number from the `GET /api/v1/deposits/methods` instructions for the `direct_deposit` method).
- Account number: from `GET /api/v1/accounts/checking` → `account_number`

A "Download Form PDF" button should generate a pre-filled direct deposit authorization form. This is a future feature — for now show the account details in a copyable format.

---

## 27. P2P Transfer Deposit

```
POST /api/v1/deposits/p2p
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 75.00,
  "account_id": "uuid-of-target-account",
  "notes": "Rent split"
}
```

Success response `data`: same base deposit object.

> **Note on P2P sender lookup:** The current implementation records the deposit on the receiver's side. The sender username (`from_username`) is not yet validated against the users table in this endpoint — the `notes` field is used for context. A proper P2P send/receive flow will be implemented in the transfers phase. For now, this records the incoming P2P deposit as pending.

---

## 28. Deposit History

```
GET /api/v1/deposits/history?page=1&per_page=20
Authorization: Bearer <access_token>
```

Query params:
- `page`: integer ≥ 1, default 1
- `per_page`: integer 1–100, default 20

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "method": "ach",
      "amount": 1000.00,
      "fee": 0.00,
      "net_amount": 1000.00,
      "status": "pending",
      "reference": "DEP-B8L3N1",
      "currency": "USD",
      "created_at": "2026-06-20T14:30:00",
      "admin_notes": null
    },
    {
      "id": "uuid",
      "method": "crypto_eth",
      "amount": 250.00,
      "fee": 0.00,
      "net_amount": 250.00,
      "status": "approved",
      "reference": "DEP-X7K2M9",
      "currency": "USD",
      "created_at": "2026-06-18T09:15:00",
      "admin_notes": "Confirmed on-chain tx 0xabc..."
    }
  ],
  "page": 1,
  "per_page": 20,
  "total": 2
}
```

**`method` field values in history:**

| Value | Display label |
|---|---|
| `ach` | ACH Transfer |
| `wire` | Wire Transfer |
| `check` | Mobile Check |
| `cash` | Cash Deposit |
| `direct_deposit` | Direct Deposit |
| `p2p` | P2P Transfer |
| `crypto_btc` | Bitcoin Deposit |
| `crypto_eth` | Ethereum Deposit |
| `crypto_usdc_erc20` | USDC Deposit |
| `crypto_usdt_trc20` | USDT Deposit |

When `status` is `rejected`, show `admin_notes` as the reason if it is not null.

---

## 29. Phase 4 Screens to Build

- [ ] Deposit Method Selection — grid/list of all 7 methods (from `GET /deposits/methods`)
- [ ] Crypto: Network Selection (BTC / ETH / USDC / USDT)
- [ ] Crypto: Amount Entry
- [ ] Crypto: Deposit Address Screen — address, QR code, copy button, deep link, countdown timer
- [ ] Crypto: Awaiting Confirmation Screen — status polling
- [ ] ACH: Amount + optional notes form
- [ ] Wire: Instructions display + amount form
- [ ] Check: Amount entry + camera capture UI (images not yet processed)
- [ ] Cash: Partner locations list + amount + reference code display
- [ ] Direct Deposit: Banking details display (routing + account) + amount form
- [ ] P2P: Amount + memo form
- [ ] All Methods: Post-submission confirmation screen showing reference number
- [ ] Deposit History — paginated list with method label, amount, status badge, reference

---

## 30. Key Notes for Phase 4

- **All deposits start as `pending`** — never show a balance increase immediately. Always show a "pending approval" message.
- **`GET /deposits/methods` is the source of truth** for what to show. Never hardcode the method list — if `is_enabled` is false, hide the method.
- **`min_amount` / `max_amount`** from the methods endpoint should be used for client-side form validation before submitting.
- **Crypto deposit sessions expire in 24 hours.** Show a countdown. If expired, the user needs to initiate a new session.
- **`qr_code` is a base64 PNG string** — use it as `<img src={qr_code} />` directly. No external QR library needed on the frontend.
- **`deep_link`** launches the user's installed crypto wallet app (Coinbase, MetaMask, Trust Wallet, etc.). Wrap it in a try/catch — if no wallet app is installed, show a fallback message.
- **Crypto method field in history** is `crypto_{network_slug}` (e.g., `crypto_eth`). Map this to a human-readable label when displaying.
- **`admin_notes`** on a rejected deposit contains the rejection reason from the admin. Always display this when `status === "rejected"`.
- **`fee` is currently 0 for all methods.** The fee system exists in the model and will be activated in a future phase — build the UI to show it but don't rely on it being non-zero yet.


---

# PHASE 5 — Withdrawals (All Methods)

> All withdrawal endpoints require `Authorization: Bearer <access_token>`.
> Base path: `/api/v1/withdrawals/...`

---

## 31. Withdrawal Concepts

### How withdrawals differ from deposits

- Withdrawals check `available_balance` **before creating the record.** If funds are insufficient the request fails immediately with `"Insufficient funds"` — no record is created.
- The balance is **not deducted** until an admin approves. The balance stays the same until approval — but since `available_balance` is checked at submission time, the user can't double-submit for more than they have.
- Like deposits, all withdrawals start in `pending` status and require admin approval.

### Withdrawal status values

Same status set as deposits — always handle all four:

| Status | Meaning | What to show |
|---|---|---|
| `pending` | Submitted, awaiting admin | "Pending" badge (yellow) |
| `approved` | Approved, funds deducted | "Completed" badge (green) |
| `rejected` | Admin rejected it | "Rejected" badge (red) + show `admin_notes` |
| `cancelled` | Cancelled before processing | "Cancelled" badge (grey) |

### Withdrawal response object

Every withdrawal method returns the same shape on success:

```json
{
  "reference": "WTH-K9M2P4",
  "withdrawal_id": "uuid",
  "amount": 500.00,
  "fee": 0.00,
  "net_amount": 500.00,
  "status": "pending"
}
```

- `reference` — unique tracking number starting with `WTH-`. Show this to the user.
- `net_amount` — `amount - fee`. This is what actually leaves the account when approved.
- `fee` — varies by method (see fee table below).

### Fee reference table

Fees come from `GET /withdrawals/methods` but here are the defaults configured in the system:

| Method | Fee | Processing Time |
|---|---|---|
| Crypto | $0.00 | 1–3 business days |
| ACH Transfer | $0.00 | 2–3 business days |
| Wire Transfer | $25.00 | 1–2 business days |
| Card Payout | $1.50 | Minutes |
| Cash Pickup | $3.00 | Same day |
| Check by Mail | $0.00 | 5–7 business days |
| Internal Transfer | $0.00 | Instant |

> **Note:** The current endpoint implementations all pass `fee=0.0` to the service regardless of method. The fee constants above are the **configured** values in the system and will be enforced in a future update. Build the UI to display the fee from the methods endpoint, but do not rely on it being deducted from `net_amount` yet.

### Source account

All withdrawal endpoints currently withdraw from the user's **checking account automatically**. There is no `account_id` field in the current endpoint implementations — the backend finds the checking account. This will be made configurable in a future update.

---

## 32. Get Withdrawal Methods

```
GET /api/v1/withdrawals/methods
```

**No auth required.**

Returns all available withdrawal methods from the database. Use this — never hardcode the list.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "name": "Crypto",
    "slug": "crypto",
    "description": "Withdraw to external crypto wallet",
    "is_enabled": true,
    "min_amount": 0.01,
    "max_amount": 1000000.0,
    "fee_type": "flat",
    "fee_amount": 0.0,
    "processing_time": null,
    "icon": "bitcoin"
  },
  {
    "id": "uuid",
    "name": "Wire Transfer",
    "slug": "wire",
    "description": "Send a wire transfer",
    "is_enabled": true,
    "min_amount": 1.0,
    "max_amount": 1000000.0,
    "fee_type": "flat",
    "fee_amount": 25.0,
    "processing_time": "1-2 business days",
    "icon": "wire"
  }
]
```

The 7 method slugs are: `crypto`, `ach`, `wire`, `card_payout`, `cash_pickup`, `check_mail`, `internal`.

- Only show methods where `is_enabled: true`.
- Use `fee_amount` to display the fee on the withdrawal form before the user submits.
- Use `min_amount` / `max_amount` for client-side validation.
- Use `processing_time` to set user expectations on the confirmation screen.

---

## 33. Crypto Withdrawal

```
POST /api/v1/withdrawals/crypto
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 500.00,
  "notes": "Withdraw to cold storage"
}
```

- `amount`: float > 0
- `notes`: optional free-text. Use this for the destination wallet address and network until the full crypto withdrawal form is wired in.

Success response `data`:
```json
{
  "reference": "WTH-K9M2P4",
  "withdrawal_id": "uuid",
  "amount": 500.00,
  "fee": 0.00,
  "net_amount": 500.00,
  "status": "pending"
}
```

> **Form guidance:** The full `CryptoWithdrawalRequest` schema in the codebase has `address` (min 10 chars) and `network` fields. These will be wired into the endpoint in a future update. For now collect them in the form and pass them via `notes` as a JSON string: `"notes": "address=0xABC...&network=eth"`. This ensures the admin panel has the destination info.

**On the withdrawal form, collect:**
- Destination wallet address
- Network (BTC / ETH / USDC ERC-20 / USDT TRC-20)
- Amount

---

## 34. ACH Withdrawal

```
POST /api/v1/withdrawals/ach
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 1000.00,
  "notes": "Transfer to Chase checking ****4521"
}
```

- `amount`: float > 0
- `notes`: optional. Use to capture destination bank details for admin reference.

Success response `data`: standard withdrawal object (reference, withdrawal_id, amount, fee, net_amount, status).

> **Form guidance:** The full `AchWithdrawalRequest` schema supports `linked_account_id`, `routing_number`, `account_number`, and `bank_name`. Until the endpoint is updated, pre-fill `notes` with the linked account info. Show the user's saved linked accounts (from `GET /users/linked-accounts`) and let them select one — then include the bank name and masked account number in the `notes` field.

---

## 35. Wire Withdrawal

```
POST /api/v1/withdrawals/wire
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 5000.00,
  "notes": "Wire to Wells Fargo - John Doe - routing 121000248 - acct 4567890123"
}
```

- `amount`: float > 0
- `notes`: optional — include all wire details here for admin processing.

Fee: **$25.00** (shown from methods endpoint, not yet deducted automatically).

> **Form guidance:** The full `WireWithdrawalRequest` schema has `bank_name`, `routing_number`, `account_number`, `recipient_name`, `swift`, and `recipient_address`. Collect all of these in the form and concatenate into the `notes` field for admin reference until the endpoint is updated. Make it clear to the user that the $25 wire fee will be deducted from the withdrawn amount upon approval.

**On the withdrawal form, collect:**
- Recipient name
- Bank name
- Routing number (9 digits)
- Account number
- SWIFT/BIC code (optional, for international)
- Recipient address (optional)

---

## 36. Card Payout

```
POST /api/v1/withdrawals/card_payout
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 200.00,
  "notes": "Debit card ending 4521"
}
```

- `amount`: float > 0
- `notes`: optional — include card details here.

Fee: **$1.50**. Processing time: **Minutes**.

> **Form guidance:** The full `CardPayoutRequest` schema has a `card_number` field (15–16 digits). Collect the card number in the form and pass it in `notes` (masked — only last 4 digits) for the admin. Never log or display full card numbers in the UI.

**On the withdrawal form, collect:**
- Debit card number (show only last 4 after entry)
- Amount

---

## 37. Cash Pickup

```
POST /api/v1/withdrawals/cash_pickup
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 150.00,
  "notes": "CVS on Broadway, New York"
}
```

- `amount`: float > 0
- `notes`: optional — user can note their preferred pickup location.

Fee: **$3.00**. Processing time: **Same day**.

After submission, display the `reference` (e.g., `WTH-K9M2P4`) as the **pickup code** the user shows at the partner location. Tell the user to bring a valid ID.

> **Pickup locations:** A live location finder endpoint is planned for a future phase. For now display a static list of partner networks: MoneyGram, Western Union, Walmart, CVS.

---

## 38. Check by Mail

```
POST /api/v1/withdrawals/check_mail
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 750.00,
  "notes": "Payee: John Doe - memo: Refund"
}
```

- `amount`: float > 0
- `notes`: optional — include payee name and memo here.

Fee: **$0.00**. Processing time: **5–7 business days**.

> **Form guidance:** The full `CheckMailRequest` schema has `payee_name`, `memo`, and `use_mailing_address` (bool). Collect these in the form and include them in `notes`. Before submitting, show the user their address on file (from `GET /users/profile`) and ask them to confirm it. If `use_mailing_address` is true, show the mailing address instead of primary address.

**On the withdrawal form, collect:**
- Payee name (defaults to user's full name)
- Memo line (optional)
- Address confirmation toggle (primary vs mailing)

---

## 39. Internal Transfer (to another BankApp user)

```
POST /api/v1/withdrawals/internal
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "amount": 50.00,
  "notes": "recipient=janedoe memo=Lunch split"
}
```

- `amount`: float > 0
- `notes`: optional — include recipient username and memo here.

Fee: **$0.00**. Processing time: **Instant** (pending admin approval in the current implementation).

> **Form guidance:** The full `InternalTransferRequest` schema has `recipient_username` and `memo`. Collect these in the form. The full recipient lookup and real-time transfer will be implemented in the transfers phase — for now pass `recipient_username` in `notes`. Show the user a warning that the transfer is subject to admin review.

**On the withdrawal form, collect:**
- Recipient username (search/autocomplete from contacts or beneficiaries)
- Memo (optional, shown to recipient)
- Amount

---

## 40. Withdrawal History

```
GET /api/v1/withdrawals/history?page=1&per_page=20
Authorization: Bearer <access_token>
```

Query params:
- `page`: integer ≥ 1, default 1
- `per_page`: integer 1–100, default 20

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "method": "ach",
      "amount": 1000.00,
      "fee": 0.00,
      "net_amount": 1000.00,
      "status": "pending",
      "reference": "WTH-B8L3N1",
      "currency": "USD",
      "created_at": "2026-06-20T14:30:00"
    },
    {
      "id": "uuid",
      "method": "wire",
      "amount": 5000.00,
      "fee": 25.00,
      "net_amount": 4975.00,
      "status": "approved",
      "reference": "WTH-X7K2M9",
      "currency": "USD",
      "created_at": "2026-06-18T09:15:00"
    }
  ],
  "page": 1,
  "per_page": 20,
  "total": 2
}
```

**`method` field display mapping:**

| Value | Display label |
|---|---|
| `crypto` | Crypto Withdrawal |
| `ach` | ACH Transfer |
| `wire` | Wire Transfer |
| `card_payout` | Card Payout |
| `cash_pickup` | Cash Pickup |
| `check_mail` | Check by Mail |
| `internal` | Internal Transfer |

---

## 41. Insufficient Funds Error

When the user's `available_balance` is less than the requested `amount`, the endpoint returns:

```json
{
  "success": false,
  "message": "Insufficient funds"
}
```

Handle this before submission where possible — read `available_balance` from `GET /accounts/balances` and validate client-side. Still handle the server-side error gracefully.

---

## 42. Phase 5 Screens to Build

- [ ] Withdrawal Method Selection — grid/list from `GET /withdrawals/methods`
- [ ] Crypto Withdrawal: network + address + amount form
- [ ] ACH Withdrawal: linked account selector + amount form
- [ ] Wire Withdrawal: recipient bank details form + amount + fee disclosure
- [ ] Card Payout: card number entry + amount form
- [ ] Cash Pickup: location info + amount + post-submit pickup code display
- [ ] Check by Mail: payee name + address confirmation + memo + amount form
- [ ] Internal Transfer: username search + memo + amount form
- [ ] All Methods: confirmation screen (shows fee, net amount, processing time) before final submit
- [ ] All Methods: success screen with reference number
- [ ] Withdrawal History — paginated list with method label, amount, fee, net amount, status badge

---

## 43. Key Notes for Phase 5

- **Check `available_balance` client-side** before enabling the submit button. Disable it and show an "Insufficient funds" message if the entered amount exceeds `available_balance`.
- **Always show fee and net_amount** on a confirmation step before the user hits submit — especially for wire ($25), card payout ($1.50), and cash pickup ($3.00).
- **References start with `WTH-`** (vs `DEP-` for deposits). Use this to distinguish them in a combined transaction history view.
- **Cash pickup `reference` is the pickup code** — display it prominently after submission with instructions to show it at the partner location with a valid ID.
- **Internal transfers are not instant yet** — even though the method says "Instant", they still go through admin approval in the current build. Don't promise real-time delivery in the UI. Label it as "Typically instant, subject to review."
- **All endpoints currently withdraw from checking** — there is no account selector yet. The source account selector will be added when the full form fields are wired in. Inform the user of this by showing "Withdrawing from: Primary Checking" on the form.
- **`notes` field is the workaround for extra data** until the rich schemas are fully wired into the endpoints. Always collect all relevant form fields and pack the important ones into `notes` so admins have the full picture.
- **No `admin_notes` field on withdrawal history items yet** — it exists on the model and will appear in a future endpoint update. Build space for it in the rejected state UI.


---

# PHASE 6 — Transfers

> All transfer endpoints require `Authorization: Bearer <access_token>`.
> Base path: `/api/v1/transfers/...`

---

## 44. Transfer Concepts

### The critical split: internal vs everything else

This is the most important thing to understand in Phase 6:

| Transfer type | Status on submit | Balance impact | Admin approval needed |
|---|---|---|---|
| `internal` | `completed` ✅ | Balance moves **immediately** | No |
| `external` | `pending` | `available_balance` reduced immediately | Yes |
| `wire` | `pending` | `available_balance` reduced immediately (amount + $25 fee) | Yes |
| `international` | `pending` | `available_balance` reduced immediately (amount + $35 fee) | Yes |

**Internal transfers between the user's own accounts (checking ↔ savings) settle instantly.** The `balance` and `available_balance` on both accounts update in real time. Refresh account balances after a successful internal transfer.

All other types reduce `available_balance` at submission time (to prevent double-spending) but the actual `balance` deduction and credit to the recipient happens when an admin approves.

### Transfer reference prefixes

| Type | Reference prefix | Example |
|---|---|---|
| Internal | `TRF-` | `TRF-A3K9M2` |
| External | `TRF-` | `TRF-B7P4N1` |
| Wire | `WIR-` | `WIR-X2L8Q5` |
| International | `INT-` | `INT-C5R1W7` |

### Transfer status values

| Status | Meaning |
|---|---|
| `completed` | Settled — only internal transfers reach this immediately |
| `pending` | Submitted, awaiting admin approval |
| `approved` | Admin approved, funds fully moved |
| `rejected` | Admin rejected — show `admin_notes` as reason |
| `cancelled` | Cancelled before processing |

### Fee summary

| Type | Fee | Who pays |
|---|---|---|
| Internal | $0.00 | — |
| External (ACH) | $0.00 | — |
| Wire | **$25.00** | Deducted from sender's `available_balance` on top of amount |
| International | **$35.00** | Deducted from sender's `available_balance` on top of amount |

For wire and international, the check is `available_balance >= amount + fee`. If not, the server returns `"Insufficient funds"`. Validate this client-side: disable submit if `amount + fee > available_balance`.

---

## 45. Internal Transfer (between own accounts)

```
POST /api/v1/transfers/internal
Authorization: Bearer <access_token>
```

**This is the only transfer type that settles instantly.**

Request body:
```json
{
  "from_account_id": "uuid-checking",
  "to_account_id": "uuid-savings",
  "amount": 500.00,
  "memo": "Moving to emergency fund"
}
```

- `from_account_id`: UUID of the source account (must belong to the current user)
- `to_account_id`: UUID of the destination account (must also belong to the current user)
- `amount`: float > 0
- `memo`: optional note

Success response `data`:
```json
{
  "reference": "TRF-A3K9M2",
  "transfer_id": "uuid",
  "amount": 500.00,
  "fee": 0.00,
  "status": "completed"
}
```

**After a successful internal transfer, immediately refresh account balances** with `GET /api/v1/accounts/balances`. The balances have changed in real time.

Error cases:
```json
{ "success": false, "message": "Source account not found" }
{ "success": false, "message": "Destination account not found" }
{ "success": false, "message": "Insufficient funds" }
```

**UX flow:**
```
1. User picks source account (dropdown of their accounts)
2. User picks destination account (dropdown — excludes source)
3. User enters amount
4. Show preview: "Transfer $500 from Checking → Savings"
5. POST /transfers/internal
        ↓ success
6. Show "Transfer complete" instantly
7. Refresh both account balances
```

---

## 46. External Transfer (to another bank via ACH)

```
POST /api/v1/transfers/external
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "from_account_id": "uuid-checking",
  "amount": 1200.00,
  "recipient_name": "Jane Doe",
  "recipient_account": "9876543210",
  "recipient_routing": "021000021",
  "recipient_bank": "Chase Bank",
  "memo": "Rent payment"
}
```

Required fields: `from_account_id`, `amount`, `recipient_name`, `recipient_account`, `recipient_routing`
Optional: `recipient_bank`, `memo`

Success response `data`:
```json
{
  "reference": "TRF-B7P4N1",
  "transfer_id": "uuid",
  "amount": 1200.00,
  "fee": 0.00,
  "status": "pending"
}
```

Status is `pending` — funds are on hold (available_balance reduced) until admin approval. Tell the user: "Your transfer is being processed. ACH transfers typically take 2–3 business days."

> **Tip:** Pre-populate this form from the user's saved beneficiaries (`GET /users/beneficiaries`). Let the user select a beneficiary and auto-fill `recipient_name`, `recipient_account`, `recipient_routing`, and `recipient_bank`.

---

## 47. Wire Transfer

```
POST /api/v1/transfers/wire
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "from_account_id": "uuid-checking",
  "amount": 10000.00,
  "recipient_name": "John Smith",
  "recipient_account": "123456789012",
  "recipient_routing": "021000021",
  "recipient_bank": "Wells Fargo",
  "swift_code": "WFBIUS6S",
  "recipient_address": "456 Oak Ave, Chicago IL 60601",
  "memo": "Business payment"
}
```

Required: `from_account_id`, `amount`, `recipient_name`, `recipient_account`, `recipient_routing`, `recipient_bank`
Optional: `swift_code`, `recipient_address`, `memo`

Success response `data`:
```json
{
  "reference": "WIR-X2L8Q5",
  "transfer_id": "uuid",
  "amount": 10000.00,
  "fee": 25.00,
  "net_amount": 9975.00,
  "status": "pending"
}
```

**The $25 fee is live and enforced.** The service checks `available_balance >= amount + 25.0`. If the user has exactly $10,000 available but enters $10,000, it will fail — they need at least $10,025.

Show a fee disclosure before the user submits:
```
Transfer amount:   $10,000.00
Wire fee:          $25.00
─────────────────────────────
Total deducted:    $10,025.00
Recipient gets:    $10,000.00
```

Processing time: 1–2 business days.

---

## 48. International Transfer

```
POST /api/v1/transfers/international
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "from_account_id": "uuid-checking",
  "amount": 2000.00,
  "recipient_name": "Marie Dupont",
  "recipient_account": "FR7630006000011234567890189",
  "recipient_bank": "BNP Paribas",
  "swift_code": "BNPAFRPPXXX",
  "country": "FR",
  "currency": "EUR",
  "memo": "Family support"
}
```

Required: `from_account_id`, `amount`, `recipient_name`, `recipient_account`, `recipient_bank`, `swift_code`, `country`
Optional: `currency` (defaults to `"USD"`), `memo`

Success response `data`:
```json
{
  "reference": "INT-C5R1W7",
  "transfer_id": "uuid",
  "amount": 2000.00,
  "fee": 35.00,
  "net_amount": 1965.00,
  "exchange_rate": 0.92,
  "converted_amount": 1840.00,
  "status": "pending"
}
```

**Currency conversion logic (current mock rates):**
- `EUR`: rate = `0.92` (1 USD = 0.92 EUR)
- All other currencies: rate = `1.0` (no conversion applied yet)

Full multi-currency rate support is planned for a future phase. For now, only EUR has a real rate — all others pass through at 1:1.

Show a conversion summary before the user submits:
```
You send:          $2,000.00 USD
Wire fee:          $35.00
─────────────────────────────
Total deducted:    $2,035.00 USD
Exchange rate:     1 USD = 0.92 EUR
Recipient gets:    €1,840.00 EUR
```

`converted_amount` and `exchange_rate` are in the response — use them directly for the confirmation screen.

---

## 49. Transfer Templates

Templates let users save frequently used transfer setups for quick repeat transfers.

### Save a template

```
POST /api/v1/transfers/templates
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "name": "Pay Mom",
  "transfer_type": "external",
  "from_account_id": "uuid-checking",
  "amount": 200.00,
  "recipient_name": "Mary Smith",
  "recipient_account": "9876543210",
  "recipient_routing": "021000021",
  "recipient_bank": "Chase",
  "memo": "Monthly support",
  "frequency": "monthly"
}
```

All `recipient_*` and `to_account_id` fields are optional depending on `transfer_type`:
- `internal`: needs `to_account_id`, skip recipient fields
- `external`: needs `recipient_name`, `recipient_account`, `recipient_routing`
- `wire`: needs all recipient fields + optionally `swift_code`
- `international`: needs all recipient fields + `swift_code`

`frequency` values: `once`, `weekly`, `biweekly`, `monthly`, `quarterly` — or `null` for no recurrence.

`transfer_type` values: `internal`, `external`, `wire`, `international`

Success response `data`:
```json
{
  "template_id": "uuid",
  "name": "Pay Mom"
}
```

### List templates

```
GET /api/v1/transfers/templates
Authorization: Bearer <access_token>
```

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "name": "Pay Mom",
    "transfer_type": "external",
    "amount": 200.00,
    "frequency": "monthly",
    "is_active": true
  },
  {
    "id": "uuid",
    "name": "Move to Savings",
    "transfer_type": "internal",
    "amount": 500.00,
    "frequency": "biweekly",
    "is_active": true
  }
]
```

### Delete a template

```
DELETE /api/v1/transfers/templates/{template_id}
Authorization: Bearer <access_token>
```

No request body. Returns:
```json
{ "success": true, "message": "Template deleted" }
```

Returns `success: false, message: "Not found"` if the template doesn't exist or belongs to another user.

---

## 50. Transfer History

```
GET /api/v1/transfers/history?page=1&per_page=20
Authorization: Bearer <access_token>
```

Query params:
- `page`: integer ≥ 1, default 1
- `per_page`: integer 1–100, default 20

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "transfer_type": "internal",
      "amount": 500.00,
      "fee": 0.00,
      "net_amount": 500.00,
      "status": "completed",
      "reference": "TRF-A3K9M2",
      "currency": "USD",
      "recipient_name": null,
      "memo": "Moving to emergency fund",
      "created_at": "2026-06-20T14:30:00"
    },
    {
      "id": "uuid",
      "transfer_type": "wire",
      "amount": 10000.00,
      "fee": 25.00,
      "net_amount": 9975.00,
      "status": "pending",
      "reference": "WIR-X2L8Q5",
      "currency": "USD",
      "recipient_name": "John Smith",
      "memo": "Business payment",
      "created_at": "2026-06-19T10:00:00"
    },
    {
      "id": "uuid",
      "transfer_type": "international",
      "amount": 2000.00,
      "fee": 35.00,
      "net_amount": 1965.00,
      "status": "pending",
      "reference": "INT-C5R1W7",
      "currency": "EUR",
      "recipient_name": "Marie Dupont",
      "memo": "Family support",
      "created_at": "2026-06-18T09:15:00"
    }
  ],
  "page": 1,
  "per_page": 20,
  "total": 3
}
```

**`transfer_type` display labels:**

| Value | Display label |
|---|---|
| `internal` | Own Account Transfer |
| `external` | Bank Transfer (ACH) |
| `wire` | Wire Transfer |
| `international` | International Transfer |

**Notes on history fields:**
- `recipient_name` is `null` for internal transfers — show source/destination account numbers instead, fetched from the accounts list.
- `currency` on international transfers reflects the recipient's currency (e.g., `EUR`), not the sender's — note this when displaying.
- `fee` and `net_amount` are always present — show them in the detail view.

---

## 51. Phase 6 Screens to Build

- [ ] Transfer Type Selection (Own Accounts / External / Wire / International)
- [ ] Internal Transfer: account picker (from/to) + amount + memo
- [ ] Internal Transfer: instant success screen + balance refresh
- [ ] External Transfer: recipient details form + beneficiary selector shortcut + amount + memo
- [ ] Wire Transfer: full recipient form + SWIFT field + amount + fee disclosure screen
- [ ] International Transfer: full form + currency selector + SWIFT + country + live conversion preview
- [ ] Conversion preview component (shows rate, converted amount, total deducted)
- [ ] Transfer confirmation step (fee breakdown before final submit — for wire and international)
- [ ] Transfer History: paginated list with type label, amount, fee, status badge, reference
- [ ] Transfer Detail view (from history tap)
- [ ] Templates List: with "Use" button to pre-fill a transfer form
- [ ] Save Template flow (after any transfer, offer to save as template)
- [ ] Delete Template confirmation

---

## 52. Key Notes for Phase 6

- **Internal transfers are instant** — status comes back as `completed`, not `pending`. Do not show a "pending review" message. Show a success state and immediately refresh balances.
- **Wire fee check is `amount + 25`**, not just `amount`. A user with exactly the transfer amount will get an "Insufficient funds" error. Validate client-side: `enteredAmount + 25 > available_balance` → disable submit and show "You need at least $X to cover the transfer and wire fee."
- **International fee check is `amount + 35`** — same logic as wire.
- **`exchange_rate` and `converted_amount`** are in the international transfer response — always display them on the confirmation and success screen so the user knows exactly what the recipient gets.
- **Currency conversion is EUR-only for now** — rate `0.92`. All other currencies return rate `1.0` with no real conversion. Clearly label non-EUR international transfers as "Currency conversion not yet available — USD will be sent."
- **Pre-fill external transfer forms from beneficiaries** (`GET /users/beneficiaries`) — this is the core UX shortcut. Show a "Select saved recipient" option at the top of the external transfer form.
- **Templates are saved locally in DB** — `frequency` field exists (weekly, monthly, etc.) but there is no background task running recurring transfers yet. Show frequency as informational only ("Scheduled: Monthly") and do not promise automatic execution.
- **Reference prefixes by type:** `TRF-` for internal/external, `WIR-` for wire, `INT-` for international. Use these to distinguish transfer types in combined history views without relying on `transfer_type` field alone.
- **`recipient_name` is null for internal transfers** — never try to display it. Instead show the account names/numbers from the accounts list.
- **After any successful transfer (all types)**, call `GET /api/v1/accounts/balances` to sync the latest balances — even for pending types, since `available_balance` was reduced at submission time.


---

# PHASE 7 — Bill Pay

> All bill pay endpoints require `Authorization: Bearer <access_token>`.
> Base path: `/api/v1/bills/...`

---

## 53. Bill Pay Concepts

### One endpoint handles all three payment types

There is no separate "schedule payment" endpoint — the single `POST /bills/pay` endpoint handles one-time, future-scheduled, and recurring payments based on which fields you include:

| Payment type | How to trigger |
|---|---|
| One-time, pay now | `scheduled_date: null`, `is_recurring: false` |
| One-time, pay on future date | `scheduled_date: "2026-07-15"`, `is_recurring: false` |
| Recurring | `is_recurring: true`, `frequency: "monthly"`, `scheduled_date: "2026-07-01"` (first payment date) |

When `is_recurring: true` and `frequency` is provided, the service automatically creates a `BillSchedule` record in addition to the payment record. The schedule drives future payments.

### Bill payment status values

| Status | Meaning |
|---|---|
| `pending` | Submitted — all bill payments start here |
| `approved` | Admin processed it |
| `rejected` | Admin rejected — show `admin_notes` |
| `cancelled` | Cancelled by user or system |

All payments start as `pending`. Balance is checked at submission (`available_balance >= amount`) but funds are not deducted until admin approval.

### Reference prefix

All bill payments use the prefix `BIL-` (e.g., `BIL-K4P9R2`).

### Frequency values

Used in both `MakePaymentRequest` and `BillSchedule`:

| Value | Meaning |
|---|---|
| `once` | One-time (no schedule created) |
| `weekly` | Every week |
| `biweekly` | Every two weeks |
| `monthly` | Once a month |
| `quarterly` | Every 3 months |

---

## 54. Payee Management

A payee is a saved biller — utility company, landlord, credit card, etc. Payees must exist before a payment can be made. `payee_id` is required on the payment endpoint.

### Add a payee

```
POST /api/v1/bills/payees
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "name": "Con Edison",
  "account_number": "ACC-4821039",
  "address": "PO Box 1702, New York NY 10116",
  "phone": "1800752636",
  "category": "utilities",
  "nickname": "Electric Bill"
}
```

Required: `name` (1–200 chars)
Optional: `account_number`, `address`, `phone`, `category`, `nickname`

`category` is a free-text string — suggested values to offer in a dropdown: `utilities`, `rent`, `mortgage`, `insurance`, `phone`, `internet`, `credit_card`, `loan`, `subscription`, `other`.

Success response `data`:
```json
{
  "payee_id": "uuid",
  "name": "Con Edison"
}
```

### List payees

```
GET /api/v1/bills/payees
Authorization: Bearer <access_token>
```

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "name": "Con Edison",
    "account_number": "ACC-4821039",
    "category": "utilities",
    "nickname": "Electric Bill"
  },
  {
    "id": "uuid",
    "name": "Chase Sapphire",
    "account_number": "4111-XXXX-XXXX-1234",
    "category": "credit_card",
    "nickname": "Chase CC"
  }
]
```

Note: `address` and `phone` are stored but not returned in the list response — only in the detail context. This is by design to keep the list lightweight.

### Update a payee

```
PUT /api/v1/bills/payees/{payee_id}
Authorization: Bearer <access_token>
```

Request body — all fields optional, send only what changed:
```json
{
  "nickname": "Con Ed Electric",
  "account_number": "ACC-4821040"
}
```

Returns:
```json
{ "success": true, "message": "Payee updated" }
```

Returns `success: false, message: "Not found"` if payee doesn't exist or belongs to another user.

### Delete a payee

```
DELETE /api/v1/bills/payees/{payee_id}
Authorization: Bearer <access_token>
```

No request body.

Returns:
```json
{ "success": true, "message": "Payee deleted" }
```

> **Note:** Deleting a payee uses `ondelete="SET NULL"` on the FK — existing payment history records are preserved with `payee_id: null`. The payee name won't be available on old records after deletion. Store payee names in your local state or cache before deletion if you want to show them in history.

---

## 55. Make a Payment

```
POST /api/v1/bills/pay
Authorization: Bearer <access_token>
```

This single endpoint handles all three payment types.

### One-time payment (pay immediately)

```json
{
  "payee_id": "uuid",
  "account_id": "uuid-checking",
  "amount": 120.00,
  "scheduled_date": null,
  "is_recurring": false,
  "frequency": null,
  "memo": "March electric bill"
}
```

### One-time payment (pay on future date)

```json
{
  "payee_id": "uuid",
  "account_id": "uuid-checking",
  "amount": 120.00,
  "scheduled_date": "2026-07-15",
  "is_recurring": false,
  "frequency": null,
  "memo": "July electric bill"
}
```

### Recurring payment

```json
{
  "payee_id": "uuid",
  "account_id": "uuid-checking",
  "amount": 1500.00,
  "scheduled_date": "2026-07-01",
  "is_recurring": true,
  "frequency": "monthly",
  "memo": "Monthly rent"
}
```

**Required fields:** `payee_id`, `account_id`, `amount`
**Optional fields:** `scheduled_date`, `is_recurring` (default `false`), `frequency`, `memo`

`scheduled_date` format: ISO 8601 date string — `"YYYY-MM-DD"` (e.g., `"2026-07-15"`). Send `null` or omit for immediate processing.

Success response `data`:
```json
{
  "reference": "BIL-K4P9R2",
  "payment_id": "uuid",
  "amount": 120.00,
  "status": "pending"
}
```

Error cases:
```json
{ "success": false, "message": "Account not found" }
{ "success": false, "message": "Insufficient funds" }
```

When `is_recurring: true`, a schedule record is also created automatically. The user can see and manage it via the schedules endpoints.

---

## 56. Scheduled Payments (Recurring)

### List active schedules

```
GET /api/v1/bills/schedules
Authorization: Bearer <access_token>
```

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "amount": 1500.00,
    "frequency": "monthly",
    "next_payment_date": "2026-07-01",
    "is_active": true,
    "memo": "Monthly rent"
  },
  {
    "id": "uuid",
    "amount": 80.00,
    "frequency": "biweekly",
    "next_payment_date": "2026-06-28",
    "is_active": true,
    "memo": null
  }
]
```

> **Known gap:** The schedule list response does not include `payee_name` — it only returns the schedule fields. To show the payee name alongside each schedule, cross-reference using your locally stored payees list from `GET /bills/payees`. Match schedules to payees by `payee_id` (stored in the model but not currently returned in the list). A future update will include `payee_name` in the schedule response.

`next_payment_date` is a string in the format that was passed during creation — always send and display as `"YYYY-MM-DD"`.

### Cancel a schedule

```
DELETE /api/v1/bills/schedules/{schedule_id}
Authorization: Bearer <access_token>
```

No request body.

Returns:
```json
{ "success": true, "message": "Schedule cancelled" }
```

Cancelling a schedule removes the `BillSchedule` record — it does not cancel any payment records that were already created. Past payments remain in history.

---

## 57. Payment History

```
GET /api/v1/bills/history?page=1&per_page=20
Authorization: Bearer <access_token>
```

Query params:
- `page`: integer ≥ 1, default 1
- `per_page`: integer 1–100, default 20

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "amount": 120.00,
      "fee": 0.00,
      "status": "pending",
      "reference": "BIL-K4P9R2",
      "scheduled_date": null,
      "is_recurring": false,
      "memo": "March electric bill",
      "created_at": "2026-06-20T14:30:00"
    },
    {
      "id": "uuid",
      "amount": 1500.00,
      "fee": 0.00,
      "status": "approved",
      "reference": "BIL-R2M8W1",
      "scheduled_date": "2026-06-01",
      "is_recurring": true,
      "memo": "Monthly rent",
      "created_at": "2026-05-25T09:00:00"
    }
  ],
  "page": 1,
  "per_page": 20,
  "total": 2
}
```

> **Known gap:** The history response does not include `payee_name` or `payee_id`. To show the payee name in history, cross-reference with your locally stored payees from `GET /bills/payees`. A future update will join payee info into the history response.

`scheduled_date` is `null` for immediate payments. For scheduled/recurring payments it holds the date string that was submitted.

`is_recurring: true` entries are recurring payment instances — use this flag to show a recurring badge (e.g., a loop/repeat icon) in the history list.

---

## 58. Bill Pay UX Flows

### One-time payment flow

```
1. GET /bills/payees → show payee list
2. User selects payee (or taps "Add Payee" → POST /bills/payees)
3. User enters amount
4. User selects source account (GET /accounts/balances)
5. Confirm screen: payee name, amount, account, date (today)
6. POST /bills/pay  { payee_id, account_id, amount }
        ↓
7. Success screen with reference BIL-XXXXXX
8. "Payment is being processed" message
```

### Scheduled / recurring payment flow

```
1–4. Same as one-time
5. User taps "Schedule for later" or "Make recurring"
   → For scheduled: show date picker → sets scheduled_date
   → For recurring: show frequency picker + first payment date
6. Confirm screen: payee, amount, account, date/frequency
7. POST /bills/pay  { payee_id, account_id, amount, scheduled_date,
                      is_recurring, frequency }
        ↓
8. Success screen with reference
9. "Next payment: [date]" message for recurring
```

### Managing recurring payments

```
1. GET /bills/schedules → show active schedules list
2. Each card shows: amount, frequency, next_payment_date
   (cross-reference payee name from GET /bills/payees)
3. User taps "Cancel" → DELETE /bills/schedules/{id}
4. Confirmation dialog before cancel
```

---

## 59. Phase 7 Screens to Build

- [ ] Bill Pay Home — payees list with "Pay" button on each, "Add Payee" CTA
- [ ] Add Payee form (name, account number, category, nickname — address/phone optional)
- [ ] Edit Payee form
- [ ] Delete Payee confirmation dialog
- [ ] Make Payment form — payee pre-selected, amount, account selector, payment type toggle
- [ ] Payment Type toggle: "Pay Now" / "Pay Later" (date picker) / "Recurring" (frequency + start date)
- [ ] Payment confirmation screen — shows payee, amount, account, date/frequency, fee ($0)
- [ ] Payment success screen — shows reference number `BIL-XXXXXX`
- [ ] Active Schedules list — each card shows amount, frequency, next date, cancel button
- [ ] Cancel Schedule confirmation dialog
- [ ] Payment History — paginated, with recurring badge, status badge, reference, amount

---

## 60. Key Notes for Phase 7

- **`POST /bills/pay` is the only payment endpoint** — one-time, scheduled, and recurring all go through it. The difference is entirely in the request fields.
- **`scheduled_date` is a plain string** — always send as `"YYYY-MM-DD"` ISO format. There is no date validation on the server beyond storing the string, so validate the date on the frontend (must be today or future for scheduled payments).
- **`is_recurring: true` requires `frequency`** — if you send `is_recurring: true` without `frequency`, the schedule record won't be created properly. Always pair them.
- **Balance is checked at submission** (`available_balance >= amount`) — but not deducted until admin approval. Do not show a balance decrease after bill pay submission.
- **Payee name is not in history or schedule responses** — cache your payees list in state and cross-reference by `payee_id`. The backend will join this in a future update but for now the frontend must handle it.
- **Deleting a payee nullifies `payee_id` on existing payments** — not the payment records themselves. If you want to show "Payee: Con Edison" on old history items, you must have cached the payee name before it was deleted.
- **Schedules do not auto-execute yet** — `next_payment_date` is informational. There is no background task running recurring bills. Display it as the intended next payment date and inform users that scheduling is subject to admin processing in the current build.
- **Fee is always `0.00`** for all bill payments. Show it in the UI for transparency but it will never be non-zero in the current build.
- **`reference` starts with `BIL-`** — use this to distinguish bill payments from transfers (`TRF-`/`WIR-`/`INT-`) and deposits/withdrawals (`DEP-`/`WTH-`) in any combined transaction view.


---

# PHASE 8 — Card Management

> All card endpoints require `Authorization: Bearer <access_token>`.
> Base path: `/api/v1/cards/...`

---

## 61. Card Concepts

### Card types and their lifecycle

| `card_type` value | Meaning |
|---|---|
| `virtual` | Active virtual card — usable for online transactions immediately |
| `physical_requested` | User has requested a physical card — waiting for delivery |
| `physical` | Physical card has been received and activated |

### Card status values

| `status` value | Meaning | What to show |
|---|---|---|
| `active` | Card is active and usable | Normal card view |
| `inactive` | Not yet activated | "Activate card" prompt |
| `reported_lost` | Reported lost/stolen — frozen permanently | "Card reported lost" banner, no unfreeze option |
| `cancelled` | Permanently cancelled | Greyed out, no actions |

### Freeze vs lost/stolen — critical UI difference

| Action | `is_frozen` | `status` | Can be unfrozen? |
|---|---|---|---|
| User freezes card | `true` | `active` | Yes — user can unfreeze |
| User reports lost/stolen | `true` | `reported_lost` | **No** — permanently locked |

Check **both** `is_frozen` and `status` to decide what to show. If `status === "reported_lost"`, do not show an unfreeze button — show a "Card reported lost. Contact support for a replacement." message.

### Card limits (defaults)

| Limit | Default |
|---|---|
| `daily_spending_limit` | $5,000.00 |
| `per_transaction_limit` | $2,500.00 |
| `atm_withdrawal_limit` | $500.00 |

### Card toggle settings (defaults)

| Setting | Default |
|---|---|
| `online_purchases` | `true` |
| `international` | `true` |
| `contactless` | `true` |
| `apple_pay` | `false` |
| `google_pay` | `false` |
| `samsung_pay` | `false` |

### Security: when to show full card details

The card detail endpoint (`GET /cards/{card_id}`) returns the **full unmasked card number** and **CVV**. The list endpoint returns masked numbers only.

Follow these display rules:
- **Card list / dashboard:** show `card_number_masked` only (e.g., `•••• •••• •••• 4521`)
- **Card detail screen:** show masked by default — reveal full number + CVV only when user taps "Show card details" and authenticates (biometric or PIN)
- **PIN:** returned **once** in plaintext at card creation only. Never stored client-side. Instruct the user to memorise it immediately.

---

## 62. List Cards

```
GET /api/v1/cards
Authorization: Bearer <access_token>
```

Returns all cards for the user — virtual and physical.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "card_type": "virtual",
    "card_number_masked": "•••• •••• •••• 4521",
    "expiry_month": "06",
    "expiry_year": "2029",
    "cardholder_name": "JOHN DOE",
    "status": "active",
    "is_frozen": false,
    "daily_spending_limit": 5000.0,
    "online_purchases": true,
    "international": true,
    "contactless": true,
    "apple_pay": false,
    "google_pay": false,
    "samsung_pay": false,
    "last_four": "4521",
    "created_at": "2026-06-01T08:00:00"
  }
]
```

`card_number_masked` is pre-formatted by the backend — use it directly. Does not include full card number or CVV.

---

## 63. Create Virtual Card

```
POST /api/v1/cards/create
Authorization: Bearer <access_token>
```

No request body needed.

The card is linked to the user's checking account. The cardholder name is auto-set to `"FIRSTNAME LASTNAME"` from the user's profile (falls back to username if no profile).

> **Note:** A virtual card is auto-created when a checking account is created (on signup). You should only need to call this if the user wants an additional card or their original card was cancelled.

Success response `data`:
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

⚠️ **`card_number`, `cvv`, and `pin` are returned in full only at creation.** This is the only time the PIN is ever available in plaintext. Show all four values in a "Save your card details" screen and instruct the user to note the PIN — it cannot be retrieved again, only verified or reset.

**Post-creation screen should show:**
- Full card number (tapable copy button)
- Expiry
- CVV (tapable copy button)
- PIN — displayed once with a "I've saved my PIN" acknowledgement before proceeding

---

## 64. Get Card Detail

```
GET /api/v1/cards/{card_id}
Authorization: Bearer <access_token>
```

Returns full card detail including the **unmasked card number** and **CVV**.

Success response `data`:
```json
{
  "id": "uuid",
  "card_number": "4532819274651234",
  "card_number_masked": "•••• •••• •••• 1234",
  "expiry_month": "06",
  "expiry_year": "2029",
  "cvv": "847",
  "cardholder_name": "JOHN DOE",
  "status": "active",
  "is_frozen": false,
  "daily_spending_limit": 5000.0,
  "per_transaction_limit": 2500.0,
  "atm_withdrawal_limit": 500.0,
  "online_purchases": true,
  "international": true,
  "contactless": true,
  "last_four": "1234"
}
```

⚠️ **Do not display `card_number` or `cvv` on screen by default.** Show the masked version. Only reveal the full number and CVV after the user explicitly taps "Show" and re-authenticates (biometric or PIN entry). This is a security requirement.

---

## 65. Freeze and Unfreeze Card

**Freeze:**
```
POST /api/v1/cards/{card_id}/freeze
Authorization: Bearer <access_token>
```

**Unfreeze:**
```
POST /api/v1/cards/{card_id}/unfreeze
Authorization: Bearer <access_token>
```

No request body for either. Both return:
```json
{ "success": true, "message": "Card frozen" }
{ "success": true, "message": "Card unfrozen" }
```

After calling either endpoint, refresh the card detail to update the `is_frozen` toggle in the UI.

**Do not allow unfreeze if `status === "reported_lost"`** — check status before showing the toggle.

---

## 66. Verify Card PIN

```
POST /api/v1/cards/{card_id}/verify-pin
Authorization: Bearer <access_token>
```

> ⚠️ This endpoint accepts a plain JSON object `{ "pin": "XXXX" }` — **not** the `PinRequest` schema. Send raw JSON.

Request body:
```json
{
  "pin": "3921"
}
```

- `pin`: exactly 4 digits as a string

Success (correct PIN):
```json
{ "success": true, "message": "PIN verified" }
```

Failure (wrong PIN):
```json
{ "success": false, "message": "Invalid PIN" }
```

Use this as a re-authentication gate before revealing full card details (number/CVV) on the card detail screen.

---

## 67. Physical Card

### Request a physical card

```
POST /api/v1/cards/{card_id}/request-physical
Authorization: Bearer <access_token>
```

No request body. Marks the virtual card as `card_type: "physical_requested"`.

Success:
```json
{ "success": true, "message": "Physical card requested" }
```

After this call, show a "Your physical card is on its way" screen. The user will receive the card in the mail (mock — 5–7 business days messaging). The card `card_type` will be `"physical_requested"` until activation.

### Activate a physical card

```
POST /api/v1/cards/{card_id}/activate
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "last_four": "1234"
}
```

- `last_four`: exactly 4 digits — the last 4 digits printed on the physical card

The backend compares this against the stored `last_four`. If they match, `card_type` is set to `"physical"` and `status` to `"active"`.

Success:
```json
{ "success": true, "message": "Card activated" }
```

Failure (wrong last 4):
```json
{ "success": false, "message": "Activation failed" }
```

**Activation UX flow:**
```
1. User receives physical card in mail
2. Opens app → Card screen shows "physical_requested" state with "Activate Card" button
3. User taps "Activate" → enters last 4 digits on card
4. POST /cards/{card_id}/activate
        ↓ success
5. Card type updates to "physical", status "active"
6. Show success screen "Card activated and ready to use"
```

---

## 68. Update Card Limits

```
PUT /api/v1/cards/{card_id}/limits
Authorization: Bearer <access_token>
```

All fields optional — send only what you want to change:

```json
{
  "daily_spending_limit": 2000.00,
  "per_transaction_limit": 1000.00,
  "atm_withdrawal_limit": 300.00
}
```

Field constraints (enforced client-side — no server-side max validation yet):
- `daily_spending_limit`: suggest max $10,000
- `per_transaction_limit`: should be ≤ `daily_spending_limit`
- `atm_withdrawal_limit`: suggest max $1,000

Success:
```json
{ "success": true, "message": "Limits updated" }
```

After updating, refresh `GET /cards/{card_id}` to show the new values.

---

## 69. Update Card Settings (Toggles)

```
PUT /api/v1/cards/{card_id}/settings
Authorization: Bearer <access_token>
```

All fields optional — send only the toggle being changed:

```json
{
  "online_purchases": false,
  "international": false,
  "contactless": true
}
```

Available toggles: `online_purchases`, `international`, `contactless`

> **Digital wallet toggles** (`apple_pay`, `google_pay`, `samsung_pay`) are **not** managed through this endpoint — they are set via the dedicated digital wallet endpoint. Don't try to set them here.

Success:
```json
{ "success": true, "message": "Settings updated" }
```

**UX pattern:** Render each toggle as an immediate-response switch. Call the endpoint on toggle change, and revert the toggle if the request fails.

---

## 70. Digital Wallet Setup

```
POST /api/v1/cards/{card_id}/digital-wallet
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "wallet_type": "apple_pay"
}
```

`wallet_type` values: `apple_pay`, `google_pay`, `samsung_pay`

This sets the corresponding boolean flag on the card to `true`. There is no "remove from wallet" endpoint — once added it stays enabled. The remove flow will be added in a future update.

Success:
```json
{ "success": true, "message": "Added to apple_pay" }
```

> **Mock implementation:** This is a backend flag only — no actual provisioning with Apple/Google/Samsung Pay APIs happens. Show the wallet as "added" in the UI based on the flag state from `GET /cards/{card_id}`. A real provisioning flow will be implemented in a future phase.

**UX flow:**
```
1. Card detail screen shows "Add to Wallet" section
2. Detect device type to show relevant wallet button
   iOS → Apple Pay
   Android → Google Pay / Samsung Pay
3. User taps "Add to Apple Pay"
4. POST /cards/{card_id}/digital-wallet  { "wallet_type": "apple_pay" }
        ↓ success
5. Show "Added to Apple Pay ✓" — button becomes inactive
6. Refresh card to confirm apple_pay: true
```

---

## 71. Card Transactions

```
GET /api/v1/cards/{card_id}/transactions
Authorization: Bearer <access_token>
```

No query params — returns all card transactions (not paginated in the current implementation).

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "amount": 42.50,
    "merchant": "Starbucks",
    "category": "food_drink",
    "status": "completed",
    "transaction_type": "purchase",
    "reference": "TXN-ABC123",
    "location": "New York, NY",
    "created_at": "2026-06-20T09:15:00"
  },
  {
    "id": "uuid",
    "amount": 200.00,
    "merchant": "Chase ATM",
    "category": "atm",
    "status": "completed",
    "transaction_type": "atm_withdrawal",
    "reference": "TXN-DEF456",
    "location": "Brooklyn, NY",
    "created_at": "2026-06-18T14:30:00"
  }
]
```

`transaction_type` values: `purchase`, `atm_withdrawal`, `refund`, `reversal`

`category` values (for display icons/labels): `food_drink`, `shopping`, `travel`, `gas`, `groceries`, `entertainment`, `utilities`, `atm`, `other`

`amount` is always positive — use `transaction_type` to determine if it's a debit or credit:
- `purchase`, `atm_withdrawal` → money out (show red/debit)
- `refund`, `reversal` → money back (show green/credit)

> **Note:** Card transactions are currently populated by the admin or test data — the card system doesn't auto-generate transactions from deposits/withdrawals yet. The transaction list may be empty until transactions are seeded.

---

## 72. File a Card Dispute

```
POST /api/v1/cards/{card_id}/dispute
Authorization: Bearer <access_token>
```

Request body:
```json
{
  "transaction_id": "uuid-of-transaction",
  "reason": "I did not make this purchase. The charge of $42.50 at Starbucks on June 20 is unauthorized."
}
```

- `transaction_id`: UUID from the card transactions list
- `reason`: 10–500 chars — must be descriptive

Success response `data`:
```json
{
  "dispute_id": "DSP-uuid-fir",
  "status": "filed",
  "reason": "I did not make this purchase..."
}
```

`dispute_id` is derived from the transaction ID (first 8 chars prefixed with `DSP-`). This is mock — no dispute tracking model exists yet. A full dispute management system will be added in a future phase.

Show the user a confirmation: "Dispute filed. Reference: DSP-XXXXXXXX. Our team will review within 3–5 business days."

---

## 73. Report Card Lost or Stolen

```
POST /api/v1/cards/{card_id}/report-lost
Authorization: Bearer <access_token>
```

No request body.

This sets `is_frozen = true` AND `status = "reported_lost"` simultaneously. Unlike a regular freeze, this cannot be reversed by the user.

Success:
```json
{ "success": true, "message": "Card reported lost" }
```

**After this call:**
- Refresh the card — show `status: "reported_lost"` state
- Hide freeze/unfreeze toggle
- Show "Card blocked permanently. Request a replacement card." message
- Show a "Request Replacement" button that triggers `POST /cards/create` (which creates a new virtual card)

**UX — show a confirmation dialog before calling this endpoint:**
```
"Report this card as lost or stolen?

This will immediately block your card and cannot be undone.
You will need to request a replacement card.

[Cancel]  [Report Lost/Stolen]"
```

---

## 74. Phase 8 Screens to Build

- [ ] Cards Home — list of all cards (virtual + physical), freeze toggle on each card
- [ ] Virtual Card Detail — masked number by default, "Show Details" → PIN/biometric gate → reveal full number + CVV + expiry
- [ ] Create Virtual Card — post-creation screen showing full number, expiry, CVV, PIN (one-time display)
- [ ] Card Settings screen — toggles for online purchases, international, contactless
- [ ] Card Limits screen — three editable limit fields with current values
- [ ] Digital Wallet section — per-wallet "Add" buttons, shows checkmark once added
- [ ] Request Physical Card flow — confirmation screen, "Card is on its way" screen
- [ ] Activate Physical Card — last 4 digits entry screen
- [ ] Card Transactions list — per card, with merchant, amount, category icon, date
- [ ] File Dispute flow — select transaction from list → reason text entry → confirmation
- [ ] Report Lost/Stolen — confirmation dialog → blocked card screen with replacement CTA
- [ ] Card replacement flow (triggers Create Virtual Card)

---

## 75. Key Notes for Phase 8

- **Virtual card is auto-created on signup** alongside the checking account. Don't show "Create Card" as a primary CTA on first load — fetch the list first and only show the create option if the list is empty.
- **PIN is returned once and never again.** The verify-pin endpoint only confirms correctness — it does not return the PIN. If the user forgets their PIN, there is no "show PIN" feature — only reset (not yet implemented). Warn users clearly at creation to save their PIN.
- **`verify-pin` takes raw `{ "pin": "XXXX" }` dict, not the `PinRequest` schema.** The endpoint reads `pin.get("pin", "")` from a plain dict. Send Content-Type: application/json with `{ "pin": "1234" }`.
- **Card detail returns full unmasked number and CVV** — call it only when needed, not on every screen load. Gate the "show card details" action behind PIN verification (`POST /cards/{card_id}/verify-pin`) before fetching and displaying the full detail.
- **`reported_lost` and `is_frozen: true` together = permanently blocked.** Always check `status` first before checking `is_frozen` to decide which UI state to show.
- **Settings and limits are separate endpoints** — `PUT /{card_id}/settings` controls `online_purchases`, `international`, `contactless`. `PUT /{card_id}/limits` controls the dollar amounts. Digital wallet flags go through `POST /{card_id}/digital-wallet`. Keep these three concerns in separate UI sections.
- **Card transactions are not paginated** in the current implementation — the endpoint returns all transactions at once. For performance, consider implementing client-side pagination if the list grows large.
- **Dispute filing is mock** — no persistence beyond the in-memory response. `dispute_id` is generated from the transaction ID at the time of the call. There is no `GET /disputes` endpoint yet. Log the `dispute_id` locally after filing so the user can reference it.
- **Digital wallet "remove" doesn't exist yet** — once `apple_pay: true`, there's no toggle-off endpoint. Don't show a "Remove" button. If the user wants to remove it, contact support (note this in the UI).
- **After any freeze/unfreeze/settings/limits update**, refresh `GET /cards/{card_id}` or `GET /cards` to sync the latest state — the API returns the result of the operation but not the updated card object.


---

# PHASE 9 — Dashboard & Transaction History

> All endpoints require `Authorization: Bearer <access_token>`.
> Dashboard base path: `/api/v1/dashboard/...`
> Unified history base path: `/api/v1/transfers/...`
> Export base path: `/api/v1/export/...`

---

## 76. Dashboard Concepts

### Transaction table vs individual method tables

Phase 9 introduces a central `transactions` table that consolidates all financial activity from every previous phase into one queryable ledger. Alongside the individual history endpoints (`/deposits/history`, `/withdrawals/history`, `/transfers/history`, `/bills/history`), there is now a unified endpoint that queries this central table directly.

**Use case split:**
- **`GET /dashboard/overview`** — home screen load, single call, gets everything you need
- **`GET /dashboard/recent-transactions`** — standalone recent feed, configurable limit
- **`GET /transfers/all`** — full transaction history with filters, search, sort, pagination
- **Individual method history endpoints** — when the user navigates to a specific section (deposits page, withdrawals page, etc.)

### Transaction type values (unified table)

Transactions in the central table use these `transaction_type` values:

| Value | Source |
|---|---|
| `deposit` | Deposit of any method |
| `withdrawal` | Withdrawal of any method |
| `transfer_internal` | Internal account-to-account transfer |
| `transfer_external` | External bank transfer |
| `transfer_wire` | Wire transfer |
| `transfer_international` | International transfer |
| `bill_payment` | Bill pay |
| `card_purchase` | Card transaction |
| `card_atm` | ATM withdrawal via card |
| `card_refund` | Card refund/reversal |
| `fee` | System fee charge |
| `interest` | Interest credit |
| `adjustment` | Admin balance adjustment |

> **Note:** The transaction table is populated by the `TransactionService.record()` method, which is called by other services when they create transactions. Not all transactions from phases 3–8 will automatically appear here — only those where the service explicitly calls `record()`. Expect gaps until each service is fully wired. Use the individual history endpoints as a fallback for complete per-method history.

---

## 77. Dashboard Overview

```
GET /api/v1/dashboard/overview
Authorization: Bearer <access_token>
```

The primary call for the home/dashboard screen. Returns everything needed in one request.

Success response `data`:
```json
{
  "total_balance": 3040.00,
  "accounts": [
    {
      "id": "uuid-checking",
      "account_number": "4820193847261",
      "account_type": "checking",
      "account_name": "Primary Checking",
      "balance": 2540.00,
      "available_balance": 2340.00,
      "pending_balance": 200.00,
      "currency": "USD",
      "is_active": true,
      "is_frozen": false,
      "interest_rate": 0.0,
      "overdraft_protection": false,
      "created_at": "2026-06-01T08:00:00"
    },
    {
      "id": "uuid-savings",
      "account_number": "5931820473652",
      "account_type": "savings",
      "account_name": "Emergency Fund",
      "balance": 500.00,
      "available_balance": 500.00,
      "pending_balance": 0.0,
      "currency": "USD",
      "is_active": true,
      "is_frozen": false,
      "interest_rate": 0.5,
      "overdraft_protection": false,
      "created_at": "2026-06-10T09:00:00"
    }
  ],
  "recent_transactions": [
    {
      "id": "uuid",
      "transaction_type": "deposit",
      "amount": 1000.00,
      "status": "completed",
      "reference": "DEP-B8L3N1",
      "description": "ACH deposit",
      "created_at": "2026-06-20T14:30:00"
    }
  ],
  "notification_count": 0,
  "pending_deposits": 0,
  "pending_withdrawals": 0
}
```

**Field breakdown:**

| Field | Use |
|---|---|
| `total_balance` | Hero balance number on home screen |
| `accounts` | Account cards list (same shape as `GET /accounts/balances`) |
| `recent_transactions` | Last 5 transactions — home screen activity feed |
| `notification_count` | Unread notification badge count (currently always `0`) |
| `pending_deposits` | Count of pending deposits (currently always `0`) |
| `pending_withdrawals` | Count of pending withdrawals (currently always `0`) |

> `notification_count`, `pending_deposits`, and `pending_withdrawals` are always `0` in the current build — these will be populated when the notification and admin approval systems are fully connected. Build the UI to handle them but don't rely on them being non-zero yet.

`recent_transactions` returns the last **5** items from the central transactions table. This is a lightweight list — no fee, net_amount, or category fields. Tap to view full detail.

---

## 78. Recent Transactions (Standalone)

```
GET /api/v1/dashboard/recent-transactions?limit=10
Authorization: Bearer <access_token>
```

Query params:
- `limit`: integer 1–50, default 10

Same response shape as `recent_transactions` in the overview, but controllable limit.

Success response `data` (array):
```json
[
  {
    "id": "uuid",
    "transaction_type": "transfer_internal",
    "amount": 500.00,
    "status": "completed",
    "reference": "TRF-A3K9M2",
    "description": "Moving to emergency fund",
    "created_at": "2026-06-20T14:30:00"
  }
]
```

Use this for a "View more" section on the dashboard that loads additional recent transactions without switching to the full history screen.

---

## 79. Unified Transaction History (Full)

```
GET /api/v1/transfers/all
Authorization: Bearer <access_token>
```

> ⚠️ **Note on URL:** Despite living under `/transfers/`, this endpoint returns **all transaction types** — deposits, withdrawals, transfers, bill payments, everything in the central `transactions` table. The path is a legacy of how the router was organised.

**All query params:**

| Param | Type | Default | Description |
|---|---|---|---|
| `page` | int ≥ 1 | `1` | Page number |
| `per_page` | int 1–100 | `20` | Items per page |
| `transaction_type` | string | — | Filter by type (see type table in section 76) |
| `status` | string | — | Filter by status: `pending`, `completed`, `approved`, `rejected` |
| `start_date` | string | — | ISO date `"YYYY-MM-DD"` — filter from this date |
| `end_date` | string | — | ISO date `"YYYY-MM-DD"` — filter to this date |
| `search` | string | — | Free-text search across description, reference, recipient |
| `sort_by` | string | `"created_at"` | Sort field: `created_at`, `amount`, `transaction_type` |
| `sort_order` | string | `"desc"` | `"asc"` or `"desc"` |

Example — filtered request:
```
GET /api/v1/transfers/all?page=1&per_page=20&transaction_type=deposit&status=pending&start_date=2026-06-01&end_date=2026-06-30&sort_by=amount&sort_order=desc
```

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "transaction_type": "deposit",
      "amount": 1000.00,
      "fee": 0.00,
      "net_amount": 1000.00,
      "currency": "USD",
      "status": "pending",
      "reference": "DEP-B8L3N1",
      "description": "ACH deposit",
      "source": "ach",
      "recipient": null,
      "category": null,
      "created_at": "2026-06-20T14:30:00"
    },
    {
      "id": "uuid",
      "transaction_type": "transfer_wire",
      "amount": 10000.00,
      "fee": 25.00,
      "net_amount": 9975.00,
      "currency": "USD",
      "status": "pending",
      "reference": "WIR-X2L8Q5",
      "description": "Wire to John Smith",
      "source": "wire",
      "recipient": "John Smith",
      "category": null,
      "created_at": "2026-06-19T10:00:00"
    }
  ],
  "total": 47,
  "page": 1,
  "per_page": 20,
  "total_pages": 3
}
```

**Response fields explained:**

| Field | Description |
|---|---|
| `total` | Total matching items across all pages |
| `total_pages` | Computed as `ceil(total / per_page)` — use for pagination controls |
| `source` | The originating method (e.g., `ach`, `wire`, `crypto_eth`) |
| `recipient` | Recipient name for transfers — `null` for deposits/internal |
| `category` | Transaction category for card transactions — usually `null` for others |
| `description` | Human-readable description of the transaction |

---

## 80. Transaction Dispute

```
POST /api/v1/disputes/transactions
Authorization: Bearer <access_token>
```

> Check the router for the exact dispute endpoint path — it may be under `/transactions/{id}/dispute`. Use Swagger at `/docs` to confirm the live URL.

Request body:
```json
{
  "transaction_id": "uuid",
  "reason": "I did not authorise this transaction. Amount of $1000 debited on June 20."
}
```

- `transaction_id`: UUID from the transactions list
- `reason`: 10–500 chars

Success response `data`:
```json
{
  "dispute_id": "uuid",
  "transaction_id": "uuid",
  "status": "open"
}
```

Dispute status values: `open`, `under_review`, `resolved`, `rejected`

Unlike the card dispute in Phase 8 (which was mock-only), this dispute is persisted in the `transaction_disputes` table and can be managed by the admin.

---

## 81. Export Endpoints

All export endpoints accept no filter params in the current implementation — they export **all** of the user's transactions. Filtering will be added in a future update.

### Export as CSV

```
GET /api/v1/export/transactions/csv
Authorization: Bearer <access_token>
```

**Returns a raw CSV file download** — not a JSON `APIResponse`. The response has:
- `Content-Type: text/csv`
- `Content-Disposition: attachment; filename=transactions.csv`

CSV columns: `date`, `type`, `amount`, `fee`, `net`, `status`, `reference`, `description`

**How to handle in the frontend:**

```javascript
// Trigger a file download
const response = await fetch('/api/v1/export/transactions/csv', {
  headers: { 'Authorization': 'Bearer ' + token }
});
const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'transactions.csv';
a.click();
window.URL.revokeObjectURL(url);
```

For React Native, use `expo-file-system` or `react-native-fs` to write the blob to the device and share it.

### Export as JSON

```
GET /api/v1/export/transactions/json
Authorization: Bearer <access_token>
```

> ⚠️ **Important:** Despite the file being named `pdf.py` on the backend, this endpoint returns **JSON data**, not a PDF. There is no PDF export in the current build.

Returns the standard `APIResponse` wrapper with `data` as a JSON string (stringified array):

```json
{
  "success": true,
  "message": "Export ready",
  "data": "[{\"date\":\"2026-06-20T14:30:00\",\"type\":\"deposit\",\"amount\":1000.0,...]"
}
```

`data` is a JSON string — parse it with `JSON.parse(response.data)` before using.

Use this for "Download JSON" or for programmatic data consumption.

### Email Transaction History

```
POST /api/v1/export/transactions/email
Authorization: Bearer <access_token>
```

No request body.

Sends a plain-text email to the user's registered email address with the subject "Your Transaction History".

> **Current state:** The email body is a placeholder — `"Your transaction history is attached."` — with no actual data attached yet. The email sending infrastructure works but the content is not built out. Show a success message to the user ("We've sent your transaction history to your email") but note internally that the content is incomplete.

Success response:
```json
{ "success": true, "message": "Export emailed" }
```

---

## 82. Recommended Dashboard Data Strategy

### On app load

```
1. GET /api/v1/dashboard/overview       (single call — balances + accounts + 5 recent txs)
        ↓
2. Render home screen with:
   - total_balance as hero number
   - account cards from accounts[]
   - recent_transactions as activity feed
   - notification badge from notification_count (0 for now)
```

### On full transaction history screen load

```
1. GET /api/v1/transfers/all?page=1&per_page=20
        ↓
2. Render list with pagination
3. Apply filters via query params on change
   - Type filter → &transaction_type=deposit
   - Date range → &start_date=2026-06-01&end_date=2026-06-30
   - Search → &search=john
   - Sort → &sort_by=amount&sort_order=desc
4. Increment page for "Load more" / pagination
```

### On pull-to-refresh

```
Re-call GET /api/v1/dashboard/overview + GET /api/v1/accounts/balances
```

### On transaction detail tap (from history)

The history endpoints don't have a `GET /transactions/{id}` detail endpoint yet. Show all available fields from the list item in a modal or detail sheet. A dedicated detail endpoint will be added in a future phase.

---

## 83. Phase 9 Screens to Build

- [ ] Dashboard / Home screen — total balance hero, account cards, recent transactions feed, notification bell
- [ ] Recent Transactions component — reusable, used on home and in "all activity" tab
- [ ] Full Transaction History screen — paginated list
- [ ] Filter drawer / bottom sheet — type, status, date range pickers
- [ ] Search bar — debounced, feeds into `&search=` query param
- [ ] Sort controls — date / amount / type, asc/desc toggle
- [ ] Transaction list item component — type icon, description, amount (colour-coded), status badge, date
- [ ] Transaction detail sheet/modal — all fields from list item in an expanded view
- [ ] File Dispute flow (from transaction detail) — reason entry, confirmation, success with dispute ID
- [ ] Export screen — "Download CSV", "Download JSON", "Email History" buttons
- [ ] CSV download trigger (browser file download or native share)
- [ ] Empty state — "No transactions yet" for new users

---

## 84. Key Notes for Phase 9

- **`GET /transfers/all` is the unified history endpoint** — despite the URL, it queries the central `transactions` table and covers all transaction types. The name is misleading but intentional based on router structure.
- **`total_pages` is pre-computed** in the history response — use it directly for pagination controls. `total` divided by `per_page` rounded up gives the same result.
- **CSV export returns raw bytes, not JSON** — don't try to parse it as `APIResponse`. Handle it as a file download using `Blob` / `Content-Disposition`.
- **JSON export `data` field is a string** — the outer wrapper is `APIResponse` with `data` as a stringified JSON array. Call `JSON.parse()` on it before iterating.
- **"PDF export" is actually JSON** — the `pdf.py` file is misnamed. There is no PDF generation in the current build. Label the button "Export JSON" or "Download Data" — not "Download PDF".
- **Email export body is a placeholder** — the email sends but contains no transaction data yet. Inform users to expect a follow-up improvement.
- **`notification_count`, `pending_deposits`, `pending_withdrawals` are always `0`** — build the badge and summary UI now, but don't show them as non-zero until the backend wires them up.
- **Recent transactions may be empty** for new users — always handle the empty array gracefully with an "No recent activity" placeholder.
- **`search` filters across description, reference, and recipient** — no need for separate search fields. One search bar covers all three.
- **`sort_by` valid values are `created_at`, `amount`, `transaction_type`** — don't pass other field names or the repository query may fail silently.
- **Transaction dispute (`POST /disputes/transactions`) is different from card dispute** (`POST /cards/{id}/dispute`) — transaction disputes are persisted to DB with a UUID, card disputes return a mock ID only. Use the transaction dispute for anything in the unified history; use card dispute only for card-specific transactions from the card screen.


---

# PHASE 10 — Notifications & Alerts

> All endpoints require `Authorization: Bearer <access_token>`.
> Notifications base path: `/api/v1/notifications/...`
> Alerts base path: `/api/v1/alerts/...`

---

## 85. Phase 10 Concepts

### Two separate systems: notifications vs alerts

These are different things — understand the split before building UI:

| System | What it is | Where managed |
|---|---|---|
| **Notifications** | In-app inbox — messages that appear in the notification centre | `/notifications/` |
| **Notification preferences** | Channel switches — whether to receive push / email / SMS | `/notifications/preferences` (Phase 2 also has `/users/notifications/preferences`) |
| **Alerts** | Trigger rules — when to fire a notification based on thresholds | `/alerts/preferences` |

A user enables `large_deposit: true` with a threshold of `$1000` (alert preference). When a deposit over $1000 lands, the system fires a notification and stores it in the notifications table. The user reads that notification in the notification centre.

### Alert sub-endpoints all do the same thing

A key finding from the code: `balance.py`, `transaction.py`, `security.py`, and `scheduled.py` under `/alerts/` are all **identical** — they all get/set the same `AlertPreference` record. There is no separate balance-only or security-only endpoint. All alert preferences are managed through one unified preferences object. Only `balance.py` is registered in the router (`prefix="/alerts"`), so the effective URLs are:

```
GET  /api/v1/alerts/preferences   ← get all alert preferences
PUT  /api/v1/alerts/preferences   ← update any/all alert preferences
```

The sub-files (`transaction.py`, `security.py`, `scheduled.py`) exist but are **not currently registered** in the router. Do not call them directly.

### Push service is currently a mock

`PushService.send()` just prints to console — no real FCM/APNs calls happen. Push notifications will not arrive on devices in the current build. The infrastructure is in place for when Firebase credentials are configured (see `.env.example` → `FIREBASE_CREDENTIALS_PATH`).

### WebSocket

A WebSocket endpoint exists in the codebase (`app/api/v1/websockets/notifications.py`) but is **not registered in the router**. Real-time push via WebSocket is not available yet. Poll the notifications list endpoint to check for new items.

---

## 86. Get Notifications

```
GET /api/v1/notifications?page=1&per_page=20
Authorization: Bearer <access_token>
```

Query params:
- `page`: integer ≥ 1, default 1
- `per_page`: integer 1–100, default 20

Success response `data`:
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Deposit Received",
      "message": "Your ACH deposit of $1,000.00 has been approved.",
      "notification_type": "deposit",
      "is_read": false,
      "reference_type": "deposit",
      "reference_id": "uuid-of-deposit",
      "created_at": "2026-06-20T14:30:00"
    },
    {
      "id": "uuid",
      "title": "Security Alert",
      "message": "New login detected from New York, US on iPhone 15 Pro.",
      "notification_type": "security",
      "is_read": true,
      "reference_type": "session",
      "reference_id": "uuid-of-session",
      "created_at": "2026-06-19T09:00:00"
    }
  ],
  "unread_count": 3,
  "page": 1,
  "per_page": 20
}
```

**Key fields:**

| Field | Use |
|---|---|
| `unread_count` | Drive the bell badge number — always reflects total unread across all pages |
| `is_read` | Show unread items with a highlight or dot indicator |
| `notification_type` | Used to pick the right icon (see type table below) |
| `reference_type` + `reference_id` | Deep-link to the related item when tapped |

**`notification_type` values and suggested icons:**

| Value | Icon | Example |
|---|---|---|
| `deposit` | ↓ arrow / green | "Deposit of $500 approved" |
| `withdrawal` | ↑ arrow / red | "Withdrawal of $200 processed" |
| `transfer` | ↔ arrows | "Transfer to Jane Doe completed" |
| `bill_payment` | receipt | "Bill payment to Con Edison sent" |
| `security` | shield / lock | "New login from New York" |
| `alert` | bell | "Balance below $100" |
| `card` | credit card | "Card frozen by admin" |
| `kyc` | document | "KYC document approved" |
| `system` | info circle | "Scheduled maintenance" |

**`reference_type` + `reference_id` deep-link targets:**

| `reference_type` | Navigation target |
|---|---|
| `deposit` | Deposit history → item with that ID |
| `withdrawal` | Withdrawal history → item with that ID |
| `transfer` | Transfer history → item with that ID |
| `bill_payment` | Bill history → item with that ID |
| `session` | Active sessions list |
| `card` | Card detail screen |
| `transaction` | Transaction history → item with that ID |
| `null` | No deep-link — notification is self-contained |

> **Note:** `total` is not returned by the list endpoint — only `unread_count` and the current page's `items`. There is no `total_pages` field. Implement "load more" pagination (append items on scroll) rather than page-number navigation.

---

## 87. Mark Notification as Read

```
PUT /api/v1/notifications/{notification_id}/read
Authorization: Bearer <access_token>
```

No request body.

```json
{ "success": true, "message": "Marked as read" }
```

Call this when the user taps a notification. Immediately update `is_read` to `true` in local state — don't wait for a refetch.

---

## 88. Mark All Notifications as Read

```
PUT /api/v1/notifications/read-all
Authorization: Bearer <access_token>
```

No request body.

```json
{ "success": true, "message": "All marked as read" }
```

After calling this, set `unread_count` to `0` and `is_read: true` on all items in local state.

---

## 89. Delete a Notification

```
DELETE /api/v1/notifications/{notification_id}
Authorization: Bearer <access_token>
```

No request body.

```json
{ "success": true, "message": "Notification deleted" }
```

Remove the item from the local list immediately on success. If `unread_count > 0` and the deleted notification was unread, decrement `unread_count` by 1 in local state.

---

## 90. Notification Channel Preferences

These control **how** notifications are delivered — push, email, or SMS. Separate from alert preferences (which control **when** to trigger).

### Get channel preferences

```
GET /api/v1/notifications/preferences
Authorization: Bearer <access_token>
```

Success response `data`:
```json
{
  "push_enabled": true,
  "email_enabled": true,
  "sms_enabled": false
}
```

Returns `data: {}` (empty object) if the user has no preferences set yet — treat as all defaults `false` for push/sms, `true` for email.

### Update channel preferences

```
PUT /api/v1/notifications/preferences
Authorization: Bearer <access_token>
```

All fields optional — send only what changed:
```json
{
  "push_enabled": true,
  "sms_enabled": true
}
```

```json
{ "success": true, "message": "Preferences updated" }
```

> **Note:** There is also a more granular notification preferences endpoint from Phase 2 at `PUT /api/v1/users/notifications/preferences` which includes per-category toggles (`push_deposits`, `email_transfers`, `sms_security`, etc.). The Phase 10 endpoint only manages the top-level channel on/off switches. Both write to the same `UserNotificationPreference` table. Use the Phase 2 endpoint for the detailed per-category settings screen and the Phase 10 endpoint for the simpler master channel toggles.

---

## 91. Alert Preferences

Alert preferences control the thresholds and rules that trigger notifications. All alert settings live in one unified preferences object — one `GET` and one `PUT` covers everything.

### Get alert preferences

```
GET /api/v1/alerts/preferences
Authorization: Bearer <access_token>
```

If no preferences exist for the user yet, the backend creates a default record automatically and returns it.

Success response `data`:
```json
{
  "balance_low": false,
  "balance_low_threshold": 100.0,
  "balance_high": false,
  "balance_high_threshold": 10000.0,
  "large_deposit": true,
  "large_deposit_threshold": 1000.0,
  "large_withdrawal": true,
  "large_withdrawal_threshold": 500.0,
  "security_login": true,
  "security_password_change": true,
  "weekly_summary": false,
  "monthly_summary": false
}
```

**Field-by-field explanation:**

| Field | Default | Meaning |
|---|---|---|
| `balance_low` | `false` | Alert when balance drops below threshold |
| `balance_low_threshold` | `100.0` | USD amount — triggers when balance goes below this |
| `balance_high` | `false` | Alert when balance exceeds threshold |
| `balance_high_threshold` | `10000.0` | USD amount — triggers when balance goes above this |
| `large_deposit` | `true` | Alert on deposits above threshold |
| `large_deposit_threshold` | `1000.0` | USD amount — deposits above this fire an alert |
| `large_withdrawal` | `true` | Alert on withdrawals above threshold |
| `large_withdrawal_threshold` | `500.0` | USD amount — withdrawals above this fire an alert |
| `security_login` | `true` | Alert on new device login |
| `security_password_change` | `true` | Alert when password is changed |
| `weekly_summary` | `false` | Weekly account summary notification |
| `monthly_summary` | `false` | Monthly account summary notification |

### Update alert preferences

```
PUT /api/v1/alerts/preferences
Authorization: Bearer <access_token>
```

All fields optional — send only what changed:

```json
{
  "balance_low": true,
  "balance_low_threshold": 250.0,
  "large_deposit_threshold": 500.0,
  "weekly_summary": true
}
```

```json
{ "success": true, "message": "Alert preferences updated" }
```

---

## 92. Recommended Alert Settings UI

Build the alerts screen as grouped sections, not a flat list:

**Balance Alerts**
```
[ ] Alert when balance falls below  [$100.00 ▾]
[ ] Alert when balance exceeds      [$10,000.00 ▾]
```

**Transaction Alerts**
```
[✓] Alert on large deposits above   [$1,000.00 ▾]
[✓] Alert on large withdrawals above [$500.00 ▾]
```

**Security Alerts** *(these are always on by default — consider locking them)*
```
[✓] New device login
[✓] Password change
```

**Summaries**
```
[ ] Weekly account summary
[ ] Monthly account summary
```

Each toggle calls `PUT /alerts/preferences` with only that boolean.
Each threshold field opens an amount input — calls `PUT /alerts/preferences` with only that threshold on confirm.

---

## 93. Polling Strategy (No WebSocket yet)

Since the WebSocket is not active, use polling to keep notifications fresh:

```
On app foreground / tab focus:
  GET /api/v1/notifications?page=1&per_page=1
  → Read unread_count from response
  → Update bell badge

Every 60 seconds while app is open:
  Same call — lightweight, only fetches 1 item to get unread_count

When user opens notification centre:
  GET /api/v1/notifications?page=1&per_page=20
  → Render full list

On pull-to-refresh in notification centre:
  Same full list call
```

The `unread_count` field is always accurate regardless of what page you fetch — a single-item fetch gives you the correct badge count without loading the full list.

---

## 94. Phase 10 Screens to Build

- [ ] Notification bell icon with unread badge (in app header/nav)
- [ ] Notification centre screen — paginated list, load more on scroll
- [ ] Notification list item — type icon, title, message preview, timestamp, unread dot
- [ ] Notification detail / expanded view (tap to expand or modal)
- [ ] Deep-link from notification tap → navigate to referenced item
- [ ] "Mark all as read" button in notification centre header
- [ ] Swipe-to-delete on notification list items
- [ ] Notification channel preferences screen (push / email / SMS master toggles)
- [ ] Alert preferences screen — grouped by category with toggles + threshold inputs
- [ ] Balance alert threshold input (numeric, USD)
- [ ] Transaction alert threshold inputs (deposit + withdrawal)
- [ ] Empty state — "No notifications yet" for new users

---

## 95. Key Notes for Phase 10

- **All four alert sub-endpoints (`balance`, `transaction`, `security`, `scheduled`) are identical** in the code — they all call the same `AlertService.get_preferences()` / `update_preferences()`. Only the `balance` router is registered at `/alerts`. Don't build separate API calls for each sub-type — one `GET /alerts/preferences` and one `PUT /alerts/preferences` covers everything.
- **`unread_count` is always the total unread** — not just for the current page. A `per_page=1` fetch still gives the correct full unread count. Use this for the bell badge without loading all notifications.
- **No `total` or `total_pages` in the notifications response** — implement infinite scroll / load-more, not page-number pagination.
- **`push_enabled` / `email_enabled` / `sms_enabled` defaults to empty object `{}`** if never set — handle gracefully by defaulting all to `false` in local state until the user explicitly sets them.
- **Push notifications don't actually send yet** — `PushService` is a console logger. The toggle can be built and saved, but users won't receive device pushes until Firebase credentials are wired in.
- **WebSocket endpoint exists but is not registered** — don't attempt a WS connection to this backend yet. Use the polling strategy from section 93.
- **`reference_type` + `reference_id` enable deep-linking** — when the user taps a notification, check `reference_type` and navigate to the appropriate screen, pre-loading or highlighting the item with `reference_id`. Always handle `null` gracefully (no navigation, just show the notification content).
- **Two notification preference endpoints exist** — `/users/notifications/preferences` (Phase 2, per-category granular) and `/notifications/preferences` (Phase 10, channel-level master toggles). They write to the same table. Show both in the settings area: master channel toggles as a quick section, detailed category preferences as an advanced section below.
- **Alert preferences auto-create on first GET** — no need to POST to create them. The service creates the default row automatically if it doesn't exist. The first time a user opens the alerts screen, call GET and display the defaults.
- **Security alerts (`security_login`, `security_password_change`) default to `true`** — these are pre-enabled for user safety. Consider showing them as locked-on with a "Recommended" label, or at minimum warn the user if they try to disable them.


---

# APPENDIX — Live API Corrections & Verified Status

> This section supersedes any uncertainty notes made in earlier phases. Everything was cross-checked against the live deployed API at `https://worldcup-orcin-chi.vercel.app/openapi.json`.

---

## A1. Production Deployment

| Item | Value |
|---|---|
| Production URL | `https://worldcup-orcin-chi.vercel.app` |
| API base | `https://worldcup-orcin-chi.vercel.app/api/v1` |
| Swagger UI | `https://worldcup-orcin-chi.vercel.app/docs` |
| ReDoc | `https://worldcup-orcin-chi.vercel.app/redoc` |
| OpenAPI JSON | `https://worldcup-orcin-chi.vercel.app/openapi.json` |
| App name | BankApp v1.0.0 |
| Environment | development |
| Host | Vercel (serverless) |

The API is fully live. All endpoints documented in Phases 1–10 are deployed and callable.

---

## A2. Corrections to Earlier Phase Notes

### Phase 10 — `/notifications/read-all` (confirmed working)

Earlier documentation flagged a possible route conflict between `PUT /notifications/{notification_id}/read` and `PUT /notifications/read-all`. **This is confirmed not a conflict.** The live OpenAPI registers them as two completely separate paths:

- `PUT /api/v1/notifications/{notification_id}/read`
- `PUT /api/v1/notifications/read-all`

Call `/read-all` directly — it works as documented.

### Phase 9 — Transaction dispute endpoint

The `POST /disputes/transactions` endpoint is **not in the live API**. The `TransactionDispute` model exists in the DB but no user-facing dispute endpoint is registered. Use the card dispute endpoint (`POST /api/v1/cards/{card_id}/dispute`) for dispute filing until a standalone transaction dispute endpoint is added.

### Phase 8 — Verify PIN confirmed as plain dict

Confirmed live: `POST /api/v1/cards/{card_id}/verify-pin` accepts `{"type": "object"}` — a plain JSON object with a `"pin"` key. Not a typed schema. Send exactly:
```json
{ "pin": "1234" }
```

### Phase 5 — Withdrawal fees

Live API confirms all withdrawal endpoints currently enforce `fee=0.0` in the service layer regardless of method. The fee constants (`$25` wire, `$1.50` card payout, `$3.00` cash pickup) are configured in the constants file but not yet applied at the endpoint level. Build the UI to display them from `GET /withdrawals/methods` but `net_amount` will equal `amount` in the current build.

### Phase 4 — Crypto networks endpoint

There is no `GET /api/v1/deposits/crypto/networks` endpoint in the live API. Use the hardcoded network list from the constants (btc, eth, usdc_erc20, usdt_trc20) to populate the network selector on the crypto deposit form.

---

## A3. Complete Live Endpoint Index

Every endpoint confirmed live on the production deployment, grouped by phase:

### Authentication (`/api/v1/auth/`)
```
POST   /auth/signup
POST   /auth/login
POST   /auth/logout
POST   /auth/verify-email
POST   /auth/resend-verification
GET    /auth/test-verification-code?email=...   ← DEV ONLY
POST   /auth/verify-phone
POST   /auth/forgot-password
POST   /auth/reset-password
POST   /auth/forgot-username
POST   /auth/refresh-token
POST   /auth/verify-2fa
POST   /auth/2fa/enable
POST   /auth/2fa/verify-setup
DELETE /auth/2fa/disable
POST   /auth/biometric/enable
POST   /auth/biometric/login
DELETE /auth/biometric/disable
```

### User Profile & Settings (`/api/v1/users/`)
```
GET    /users/profile
PUT    /users/profile
PUT    /users/password
PUT    /users/pin
GET    /users/security-questions
PUT    /users/security-questions
GET    /users/documents
POST   /users/documents/upload
GET    /users/kyc/status
GET    /users/beneficiaries
POST   /users/beneficiaries
PUT    /users/beneficiaries/{id}
DELETE /users/beneficiaries/{id}
GET    /users/linked-accounts
POST   /users/linked-accounts
POST   /users/linked-accounts/{id}/verify
DELETE /users/linked-accounts/{id}
GET    /users/limits
GET    /users/notifications/preferences
PUT    /users/notifications/preferences
GET    /users/preferences
PUT    /users/preferences
GET    /users/devices
DELETE /users/devices/{id}
GET    /users/sessions
DELETE /users/sessions/{id}
GET    /users/activity
POST   /users/close-account
```

### Accounts (`/api/v1/accounts/`)
```
GET    /accounts/checking
GET    /accounts/savings
POST   /accounts/savings
GET    /accounts/balances
GET    /accounts/{id}/balance
GET    /accounts/{id}/statements
POST   /accounts/{id}/statements/generate
```

### Deposits (`/api/v1/deposits/`)
```
GET    /deposits/methods
POST   /deposits/crypto/initiate
GET    /deposits/crypto/session/{reference}
POST   /deposits/ach
POST   /deposits/wire
POST   /deposits/check
POST   /deposits/cash
POST   /deposits/direct_deposit
POST   /deposits/p2p
GET    /deposits/history
```

### Withdrawals (`/api/v1/withdrawals/`)
```
GET    /withdrawals/methods
POST   /withdrawals/crypto
POST   /withdrawals/ach
POST   /withdrawals/wire
POST   /withdrawals/card_payout
POST   /withdrawals/cash_pickup
POST   /withdrawals/check_mail
POST   /withdrawals/internal
GET    /withdrawals/history
```

### Transfers (`/api/v1/transfers/`)
```
POST   /transfers/internal
POST   /transfers/external
POST   /transfers/wire
POST   /transfers/international
GET    /transfers/templates
POST   /transfers/templates
DELETE /transfers/templates/{id}
GET    /transfers/all              ← unified transaction history with filters
```

### Bill Pay (`/api/v1/bills/`)
```
GET    /bills/payees
POST   /bills/payees
PUT    /bills/payees/{id}
DELETE /bills/payees/{id}
POST   /bills/pay
GET    /bills/schedules
DELETE /bills/schedules/{id}
GET    /bills/history
```

### Cards (`/api/v1/cards/`)
```
GET    /cards
POST   /cards/create
GET    /cards/{id}
POST   /cards/{id}/freeze
POST   /cards/{id}/unfreeze
POST   /cards/{id}/verify-pin
POST   /cards/{id}/request-physical
POST   /cards/{id}/activate
PUT    /cards/{id}/limits
PUT    /cards/{id}/settings
GET    /cards/{id}/transactions
POST   /cards/{id}/digital-wallet
POST   /cards/{id}/dispute
POST   /cards/{id}/report-lost
```

### Dashboard (`/api/v1/dashboard/`)
```
GET    /dashboard/overview
GET    /dashboard/recent-transactions?limit=10
```

### Export (`/api/v1/export/`)
```
GET    /export/transactions/csv     ← returns raw CSV file, not JSON
GET    /export/transactions/json    ← returns APIResponse with JSON string in data
POST   /export/transactions/email   ← sends email (placeholder body)
```

### Notifications (`/api/v1/notifications/`)
```
GET    /notifications
PUT    /notifications/{id}/read
PUT    /notifications/read-all
DELETE /notifications/{id}
GET    /notifications/preferences
PUT    /notifications/preferences
```

### Alerts (`/api/v1/alerts/`)
```
GET    /alerts/preferences
PUT    /alerts/preferences
```

---

## A4. Endpoints NOT in the Live API (planned for future phases)

These were mentioned in documentation but confirmed absent from the deployed API:

| Endpoint | Status |
|---|---|
| `GET /deposits/crypto/networks` | Not deployed — use hardcoded network list |
| `POST /disputes/transactions` | Not deployed — use `POST /cards/{id}/dispute` |
| `GET /transactions/{id}` | No individual transaction detail endpoint |
| WebSocket `ws://…/notifications` | Not registered — use polling |
| `GET /users/login-history` | Model exists, no endpoint |
| `POST /users/update-email` | Model field exists, no endpoint yet |
| `POST /users/update-phone` | Model field exists, no endpoint yet |
| `GET /alerts/history` | Model exists, no endpoint |

---

## A5. Quick Start for the Frontend Developer

1. Open Swagger: `https://worldcup-orcin-chi.vercel.app/docs`
2. Create a test user: `POST /auth/signup`
3. Get the verification code: `GET /auth/test-verification-code?email=your@email.com`
4. Verify email: `POST /auth/verify-email`
5. Login: `POST /auth/login` → copy `access_token`
6. Click "Authorize" in Swagger → paste `Bearer <token>`
7. All protected endpoints are now testable directly in the browser

The test verification code endpoint (`GET /auth/test-verification-code`) is available in the live API — use it freely during development so you don't need a real email server to test the signup flow.
