import random
from datetime import datetime

def generate_card_number() -> str:
    digits = [4] + [random.randint(0,9) for _ in range(14)]
    total = 0
    for i in range(15):
        d = digits[i]
        if i % 2 == 0: d *= 2
        if d > 9: d -= 9
        total += d
    digits.append((10 - (total % 10)) % 10)
    return ''.join(str(d) for d in digits)

def generate_cvv() -> str: return str(random.randint(100, 999))
def generate_pin() -> str: return ''.join(str(random.randint(0,9)) for _ in range(4))
def generate_expiry() -> tuple:
    now = datetime.utcnow()
    month = now.month
    year = now.year + 4
    return str(month).zfill(2), str(year)

def mask_card_number(number: str) -> str:
    return f"{number[:4]} **** **** {number[-4:]}"
