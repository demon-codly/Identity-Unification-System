"""
Input validation utilities
"""
from typing import Dict, Any, List


VALID_PLATFORMS = ['email', 'whatsapp', 'dashboard', 'instagram']
VALID_STATUSES = ['active', 'inactive', 'merged']


def validate_platform(platform: str) -> bool:
    """Validate platform name"""
    return platform in VALID_PLATFORMS


def validate_identity_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate identity creation data
    Returns: (is_valid, error_messages)
    """
    errors = []
    
    # Required fields
    if not data.get('platform'):
        errors.append("Platform is required")
    elif not validate_platform(data['platform']):
        errors.append(f"Platform must be one of: {', '.join(VALID_PLATFORMS)}")
    
    if not data.get('identifier'):
        errors.append("Identifier is required")
    
    # Optional validation based on platform
    platform = data.get('platform')
    identifier = data.get('identifier')
    
    if platform == 'email' and identifier:
        if '@' not in identifier:
            errors.append("Invalid email format")
    
    if platform == 'whatsapp' and identifier:
        if not any(char.isdigit() for char in identifier):
            errors.append("Phone number must contain digits")
    
    return (len(errors) == 0, errors)
