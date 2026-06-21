"""
Date and time utility functions.
"""

from datetime import datetime, date, timedelta, timezone
from typing import Optional, Tuple
from dateutil.relativedelta import relativedelta


def now_utc() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def today() -> date:
    """Get today's date in UTC."""
    return now_utc().date()


def start_of_day(dt: Optional[datetime] = None) -> datetime:
    """Get the start of a day (00:00:00 UTC)."""
    if dt is None:
        dt = now_utc()
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: Optional[datetime] = None) -> datetime:
    """Get the end of a day (23:59:59.999999 UTC)."""
    if dt is None:
        dt = now_utc()
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def start_of_month(dt: Optional[datetime] = None) -> datetime:
    """Get the start of the current month."""
    if dt is None:
        dt = now_utc()
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def end_of_month(dt: Optional[datetime] = None) -> datetime:
    """Get the end of the current month."""
    if dt is None:
        dt = now_utc()
    next_month = dt.replace(day=28) + timedelta(days=4)
    return next_month.replace(day=1) - timedelta(microseconds=1)


def days_ago(n: int) -> datetime:
    """Get datetime N days ago."""
    return now_utc() - timedelta(days=n)


def hours_ago(n: int) -> datetime:
    """Get datetime N hours ago."""
    return now_utc() - timedelta(hours=n)


def minutes_ago(n: int) -> datetime:
    """Get datetime N minutes ago."""
    return now_utc() - timedelta(minutes=n)


def add_business_days(start_date: datetime, num_days: int) -> datetime:
    """
    Add business days (skip weekends) to a date.
    Not accounting for holidays.
    """
    current = start_date
    days_added = 0
    
    while days_added < num_days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday-Friday
            days_added += 1
    
    return current


def is_weekend(dt: datetime) -> bool:
    """Check if a date falls on a weekend."""
    return dt.weekday() >= 5


def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date."""
    today_date = today()
    age = today_date.year - birth_date.year
    if today_date.month < birth_date.month or (
        today_date.month == birth_date.month and today_date.day < birth_date.day
    ):
        age -= 1
    return age


def is_adult(birth_date: date, min_age: int = 18) -> bool:
    """Check if someone is at least min_age years old."""
    return calculate_age(birth_date) >= min_age


def format_time_ago(dt: datetime) -> str:
    """Get human-readable 'time ago' string."""
    diff = now_utc() - dt
    
    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=30):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif diff < timedelta(days=365):
        months = diff.days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = diff.days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"
