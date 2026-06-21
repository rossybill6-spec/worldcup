"""
Formatting utilities for currency, phone numbers, dates, etc.
"""

from decimal import Decimal
from typing import Optional


def format_currency(amount, currency: str = "USD") -> str:
    """
    Format a number as currency.
    Example: 1234.5 -> "$1,234.50"
    """
    if amount is None:
        return "$0.00"
    
    amount = float(amount)
    
    if currency == "USD":
        return f"${amount:,.2f}"
    
    return f"{amount:,.2f} {currency}"


def format_phone(phone: str) -> str:
    """
    Format a phone number for display.
    +1234567890 -> (234) 567-890
    """
    import re
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 11 and digits.startswith('1'):
        digits = digits[1:]
    
    if len(digits) == 10:
        return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"
    
    return phone


def format_ssn(ssn: str, masked: bool = True) -> str:
    """
    Format SSN for display.
    123456789 -> 123-45-6789 or ***-**-6789
    """
    import re
    digits = re.sub(r'\D', '', ssn)
    
    if len(digits) != 9:
        return ssn
    
    if masked:
        return f"***-**-{digits[5:9]}"
    
    return f"{digits[0:3]}-{digits[3:5]}-{digits[5:9]}"


def format_card_number(card_number: str, masked: bool = True) -> str:
    """
    Format a card number for display.
    4532123456787891 -> 4532 **** **** 7891 or 4532 1234 5678 7891
    """
    import re
    digits = re.sub(r'\D', '', card_number)
    
    if len(digits) < 4:
        return card_number
    
    if masked:
        return f"{digits[0:4]} **** **** {digits[-4:]}"
    
    # Group in 4s
    groups = [digits[i:i+4] for i in range(0, len(digits), 4)]
    return " ".join(groups)


def format_account_number(account_number: str) -> str:
    """Format account number for display: ****1234"""
    import re
    digits = re.sub(r'\D', '', account_number)
    
    if len(digits) <= 4:
        return f"****{digits}"
    
    return f"****{digits[-4:]}"


def format_date(date_obj, format_str: str = "%B %d, %Y") -> str:
    """Format a date object to string."""
    if date_obj is None:
        return ""
    return date_obj.strftime(format_str)


def format_datetime(dt_obj) -> str:
    """Format datetime to readable string."""
    if dt_obj is None:
        return ""
    return dt_obj.strftime("%B %d, %Y at %I:%M %p")


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate a string with suffix if too long."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def mask_email(email: str) -> str:
    """
    Partially mask an email for display.
    johnsmith@gmail.com -> joh*****@gmail.com
    """
    if not email or '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    
    if len(local) <= 3:
        masked_local = local[0] + "*" * (len(local) - 1)
    else:
        masked_local = local[0:3] + "*" * (len(local) - 3)
    
    return f"{masked_local}@{domain}"
