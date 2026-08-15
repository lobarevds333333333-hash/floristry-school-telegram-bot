import re
from typing import Tuple, Optional

def validate_phone(phone_str: str) -> Tuple[bool, Optional[str]]:
    """
    Validates and formats a phone number.
    Returns (is_valid, formatted_phone).
    """
    cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
    
    # Russian standard phone format matching (+7 or 8)
    if re.match(r'^(\+7|8)\d{10}$', cleaned):
        if cleaned.startswith('8'):
            formatted = '+7' + cleaned[1:]
        else:
            formatted = cleaned
        return True, formatted
    
    # Generic international format
    if re.match(r'^\+\d{10,15}$', cleaned):
        return True, cleaned

    # Raw 10-digit number without country code, assume +7
    if re.match(r'^\d{10}$', cleaned):
        return True, f'+7{cleaned}'

    return False, None


def validate_email(email_str: str) -> bool:
    """
    Validates an email address format.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email_str.strip()))
