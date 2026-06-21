"""
String manipulation utility functions.
"""

import re
import unicodedata
from typing import Optional


def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    'Hello World!' -> 'hello-world'
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')


def snake_to_title(text: str) -> str:
    """
    Convert snake_case to Title Case.
    'user_profile' -> 'User Profile'
    """
    return text.replace('_', ' ').title()


def camel_to_snake(text: str) -> str:
    """
    Convert camelCase to snake_case.
    'userProfile' -> 'user_profile'
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()


def truncate_words(text: str, num_words: int = 20, suffix: str = "...") -> str:
    """Truncate text to a number of words."""
    if not text:
        return ""
    words = text.split()
    if len(words) <= num_words:
        return text
    return " ".join(words[:num_words]) + suffix


def extract_initials(text: str, max_chars: int = 2) -> str:
    """
    Extract initials from a name.
    'John Doe' -> 'JD'
    """
    words = text.strip().split()
    initials = ''.join(w[0].upper() for w in words if w)
    return initials[:max_chars]


def normalize_name(name: str) -> str:
    """Normalize a name (title case, trim extra spaces)."""
    if not name:
        return name
    return " ".join(name.strip().title().split())


def normalize_email(email: str) -> str:
    """Normalize an email address (lowercase, strip)."""
    if not email:
        return email
    return email.strip().lower()


def normalize_phone(phone: str) -> str:
    """Normalize a US phone number to E.164 format."""
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith('1'):
        return f"+{digits}"
    return phone


def remove_special_chars(text: str, allow_spaces: bool = True) -> str:
    """Remove special characters from a string."""
    if allow_spaces:
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return re.sub(r'[^a-zA-Z0-9]', '', text)


def is_empty_or_whitespace(text: Optional[str]) -> bool:
    """Check if a string is None, empty, or only whitespace."""
    return text is None or text.strip() == ""


def safe_compare_strings(str1: str, str2: str, case_sensitive: bool = False) -> bool:
    """Safely compare two strings, handling None."""
    if str1 is None and str2 is None:
        return True
    if str1 is None or str2 is None:
        return False
    if not case_sensitive:
        return str1.strip().lower() == str2.strip().lower()
    return str1.strip() == str2.strip()
