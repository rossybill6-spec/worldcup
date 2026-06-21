"""
ID and reference number generators for transactions, accounts, cards, etc.
"""

import uuid
import random
import string
from datetime import datetime


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def generate_account_number() -> str:
    """
    Generate a realistic US bank account number (10 digits).
    First digit is 1-9, rest are random.
    """
    first = str(random.randint(1, 9))
    rest = ''.join(str(random.randint(0, 9)) for _ in range(9))
    return first + rest


def generate_routing_number() -> str:
    """
    Generate a valid US routing number (9 digits).
    Uses ABA checksum algorithm.
    """
    while True:
        digits = [random.randint(0, 9) for _ in range(8)]
        checksum = (
            3 * (digits[0] + digits[3] + digits[6])
            + 7 * (digits[1] + digits[4] + digits[7])
            + 1 * (digits[2] + digits[5])
        )
        check_digit = (10 - (checksum % 10)) % 10
        digits.append(check_digit)
        routing = ''.join(str(d) for d in digits)
        return routing


def generate_card_number() -> str:
    """
    Generate a valid 16-digit card number using Luhn algorithm.
    Starts with 4 (Visa-like).
    """
    digits = [4] + [random.randint(0, 9) for _ in range(14)]
    
    # Luhn algorithm
    total = 0
    for i in range(15):
        d = digits[i]
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    
    check_digit = (10 - (total % 10)) % 10
    digits.append(check_digit)
    
    return ''.join(str(d) for d in digits)


def generate_card_cvv() -> str:
    """Generate a 3-digit CVV."""
    return str(random.randint(100, 999))


def generate_card_pin() -> str:
    """Generate a 4-digit PIN."""
    return ''.join(str(random.randint(0, 9)) for _ in range(4))


def generate_transaction_reference(prefix: str = "TXN") -> str:
    """
    Generate a unique transaction reference.
    Format: TXN-20260621-ABC123
    """
    date_str = datetime.utcnow().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{date_str}-{random_part}"


def generate_deposit_reference() -> str:
    """Generate a deposit reference: DEP-20260621-X7K3F"""
    return generate_transaction_reference(prefix="DEP")


def generate_withdrawal_reference() -> str:
    """Generate a withdrawal reference: WTH-20260621-X7K3F"""
    return generate_transaction_reference(prefix="WTH")


def generate_transfer_reference() -> str:
    """Generate a transfer reference: TRF-20260621-X7K3F"""
    return generate_transaction_reference(prefix="TRF")


def generate_bill_payment_reference() -> str:
    """Generate a bill payment reference: BIL-20260621-X7K3F"""
    return generate_transaction_reference(prefix="BIL")


def generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP code."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def generate_referral_code() -> str:
    """Generate a user referral code: 8 characters."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_session_token() -> str:
    """Generate a unique session token."""
    return str(uuid.uuid4()) + '-' + str(uuid.uuid4())[:8]


def generate_api_key() -> str:
    """Generate an API key: bank_live_xxxx or bank_test_xxxx"""
    prefix = "bank_live"
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    return f"{prefix}_{random_part}"
