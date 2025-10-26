"""
Data normalization utilities
"""
import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from typing import Optional


def normalize_email(email: Optional[str]) -> Optional[str]:
    """
    Normalize email address:
    - Convert to lowercase
    - Trim whitespace
    - Validate format
    """
    if not isinstance(email, str) or not email:
        return None
    email = email.strip().lower()
    try:
        validated = validate_email(email, check_deliverability=False)
        return validated.normalized
    except EmailNotValidError:
        return None


def normalize_phone(phone: Optional[str]) -> Optional[str]:
    """
    Normalize phone number to E.164 format, e.g., +919876543210
    """
    if not isinstance(phone, str) or not phone:
        return None
    try:
        # Remove common formatting characters
        phone_clean = re.sub(r'[^\d+]', '', phone)
        # Parse phone number (assuming Indian numbers as default)
        parsed = phonenumbers.parse(phone_clean, "IN")
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )
    except Exception:
        pass
    return None


def normalize_name(name: Optional[str]) -> Optional[str]:
    """
    Normalize person name:
    - Title case
    - Remove extra whitespace
    - Remove special characters except spaces, hyphens, apostrophes
    """
    if not isinstance(name, str) or not name:
        return None
    # Remove extra whitespace
    name_clean = ' '.join(name.split())
    # Remove special characters except spaces, hyphens, apostrophes
    name_clean = re.sub(r"[^a-zA-Z\s'-]", '', name_clean)
    # Title case
    name_clean = name_clean.strip().title()
    return name_clean if name_clean else None


def normalize_username(username: Optional[str]) -> Optional[str]:
    """
    Normalize username/handle:
    - Convert to lowercase
    - Remove '@' symbol if present
    - Trim whitespace
    """
    if not isinstance(username, str) or not username:
        return None
    username_clean = username.strip().lower()
    if username_clean.startswith('@'):
        username_clean = username_clean[1:]
    return username_clean if username_clean else None
