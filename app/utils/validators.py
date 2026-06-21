"""
Input validation utilities for emails, phones, SSN, passwords, addresses, etc.
"""

import re
from typing import Optional, Tuple


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an email address.
    Returns (is_valid, error_message).
    """
    if not email:
        return False, "Email is required"
    
    email = email.strip().lower()
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 255:
        return False, "Email must be less than 255 characters"
    
    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a US phone number.
    Accepts formats: +1234567890, 1234567890, (123) 456-7890, 123-456-7890
    Returns (is_valid, error_message, cleaned_number).
    """
    if not phone:
        return False, "Phone number is required"
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 11 and digits.startswith('1'):
        digits = digits[1:]
    
    if len(digits) != 10:
        return False, "Phone number must be 10 digits"
    
    cleaned = f"+1{digits}"
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength.
    Requirements: min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    return True, None


def validate_ssn(ssn: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a US Social Security Number.
    Accepts formats: 123-45-6789, 123456789
    """
    if not ssn:
        return False, "SSN is required"
    
    digits = re.sub(r'\D', '', ssn)
    
    if len(digits) != 9:
        return False, "SSN must be 9 digits"
    
    if digits.startswith('000') or digits.startswith('666'):
        return False, "Invalid SSN"
    
    if digits[0:3] == '900' or int(digits[0:3]) >= 900:
        return False, "Invalid SSN"
    
    if digits[3:5] == '00':
        return False, "Invalid SSN"
    
    if digits[5:9] == '0000':
        return False, "Invalid SSN"
    
    return True, None


def validate_routing_number(routing: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a US bank routing number (ABA).
    Must be 9 digits and pass checksum.
    """
    if not routing:
        return False, "Routing number is required"
    
    digits = re.sub(r'\D', '', routing)
    
    if len(digits) != 9:
        return False, "Routing number must be 9 digits"
    
    # ABA checksum algorithm
    checksum = (
        3 * (int(digits[0]) + int(digits[3]) + int(digits[6]))
        + 7 * (int(digits[1]) + int(digits[4]) + int(digits[7]))
        + 1 * (int(digits[2]) + int(digits[5]) + int(digits[8]))
    )
    
    if checksum % 10 != 0:
        return False, "Invalid routing number"
    
    return True, None


def validate_account_number(account: str) -> Tuple[bool, Optional[str]]:
    """Validate a bank account number."""
    if not account:
        return False, "Account number is required"
    
    digits = re.sub(r'\D', '', account)
    
    if len(digits) < 4 or len(digits) > 17:
        return False, "Account number must be between 4 and 17 digits"
    
    return True, None


def validate_zip_code(zip_code: str) -> Tuple[bool, Optional[str]]:
    """Validate a US ZIP code."""
    if not zip_code:
        return False, "ZIP code is required"
    
    pattern = r'^\d{5}(-\d{4})?$'
    if not re.match(pattern, zip_code.strip()):
        return False, "Invalid ZIP code format (12345 or 12345-6789)"
    
    return True, None


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a username.
    Requirements: 4-30 chars, alphanumeric and underscore only
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 4:
        return False, "Username must be at least 4 characters"
    
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, None


def validate_amount(amount, min_amount: float = 0.01, max_amount: float = 1000000.00) -> Tuple[bool, Optional[str]]:
    """Validate a monetary amount."""
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return False, "Amount must be a valid number"
    
    if amount < min_amount:
        return False, f"Amount must be at least ${min_amount:,.2f}"
    
    if amount > max_amount:
        return False, f"Amount cannot exceed ${max_amount:,.2f}"
    
    return True, None


def validate_crypto_address(address: str, network: str) -> Tuple[bool, Optional[str]]:
    """Basic validation for crypto wallet addresses."""
    if not address:
        return False, "Address is required"
    
    network = network.lower()
    
    if network in ("bitcoin", "btc"):
        # Bitcoin addresses: 1..., 3..., bc1...
        if not re.match(r'^(1|3|bc1)[a-zA-Z0-9]{25,62}$', address):
            return False, "Invalid Bitcoin address format"
    
    elif network in ("ethereum", "eth", "erc20"):
        # Ethereum addresses: 0x followed by 40 hex chars
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return False, "Invalid Ethereum address format"
    
    elif network in ("tron", "trc20"):
        # TRON addresses: T followed by 33 chars
        if not re.match(r'^T[a-zA-Z0-9]{33}$', address):
            return False, "Invalid TRON address format"
    
    return True, None
