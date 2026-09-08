import re
from datetime import date, datetime

DOB_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
DOB_REGEX = re.compile(DOB_PATTERN)


def validate_date_of_birth(v: str) -> str:
    """
    Validate date of birth string:
    1. Strictly enforce YYYY-MM-DD pattern (reject single-digit months/days like 1985-5-1).
    2. Check valid calendar date (reject impossible dates like 2025-02-29).
    3. Check non-future date (cannot be born in future).
    4. Check reasonable minimum date (>= 1900-01-01).
    """
    if not isinstance(v, str) or not DOB_REGEX.match(v):
        raise ValueError("Invalid date format. Expected strict YYYY-MM-DD.")
    try:
        parsed_date = datetime.strptime(v, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Impossible calendar date. Expected valid YYYY-MM-DD.")
    if parsed_date > date.today():
        raise ValueError("Date of birth cannot be in the future.")
    if parsed_date < date(1900, 1, 1):
        raise ValueError("Date of birth cannot be earlier than 1900-01-01.")
    return v
