"""
Password generator utility.
"""

import random
import string


def generate_password(length: int = 16, include_uppercase: bool = True, include_lowercase: bool = True, include_numbers: bool = True, include_special: bool = True) -> str:
    """
    Generate a random password.
    
    Args:
        length: Password length (default 16)
        include_uppercase: Include uppercase letters
        include_lowercase: Include lowercase letters
        include_numbers: Include numbers
        include_special: Include special characters
    
    Returns:
        Generated password string
    """
    chars = ""
    
    if include_lowercase:
        chars += string.ascii_lowercase
    if include_uppercase:
        chars += string.ascii_uppercase
    if include_numbers:
        chars += string.digits
    if include_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    # Ensure at least one of each required type
    password = []
    if include_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if include_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if include_numbers:
        password.append(random.choice(string.digits))
    if include_special:
        password.append(random.choice("!@#$%^&*"))
    
    # Fill the rest
    remaining = length - len(password)
    password.extend(random.choice(chars) for _ in range(remaining))
    
    # Shuffle
    random.shuffle(password)
    
    return ''.join(password)


def generate_pin(length: int = 4) -> str:
    """Generate a numeric PIN."""
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def check_password_strength(password: str) -> dict:
    """
    Check password strength.
    Returns dict with score (0-100) and feedback.
    """
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 20
    else:
        feedback.append("Password should be at least 8 characters")
    
    if len(password) >= 12:
        score += 10
    
    if any(c.islower() for c in password):
        score += 20
    else:
        feedback.append("Add lowercase letters")
    
    if any(c.isupper() for c in password):
        score += 20
    else:
        feedback.append("Add uppercase letters")
    
    if any(c.isdigit() for c in password):
        score += 20
    else:
        feedback.append("Add numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 10
    else:
        feedback.append("Add special characters")
    
    return {
        "score": min(score, 100),
        "strength": "strong" if score >= 80 else "medium" if score >= 50 else "weak",
        "feedback": feedback,
    }
