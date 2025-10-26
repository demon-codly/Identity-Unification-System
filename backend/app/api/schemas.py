"""
Request/Response schemas and validation
"""
from typing import Optional, Dict, Any


class IdentitySchema:
    """Schema for identity creation"""
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate identity data"""
        required_fields = ['platform', 'identifier']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False, f"Missing required field: {field}"
        
        return True, ""


class ProfileSchema:
    """Schema for profile creation"""
    
    @staticmethod
    def validate(data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate profile data"""
        if 'canonical_name' not in data or not data['canonical_name']:
            return False, "Missing required field: canonical_name"
        
        return True, ""
