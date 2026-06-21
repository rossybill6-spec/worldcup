"""Reference code generator."""
import random, string
from datetime import datetime
def generate_reference(prefix: str = "DEP") -> str:
    date_str = datetime.utcnow().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{prefix}-{date_str}-{random_part}"
