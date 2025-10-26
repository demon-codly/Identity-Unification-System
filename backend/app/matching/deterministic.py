"""
Phase 1: Deterministic (Exact) Matching Logic
"""
from typing import Optional, Dict, Any, List
from app.database import get_db
from app.utils.normalizers import (
    normalize_email,
    normalize_phone,
    normalize_username
)


class DeterministicMatcher:
    """
    Exact matching based on normalized identifiers
    Confidence Score: 1.0 (100%)
    """
    
    def __init__(self):
        self.db = get_db()
    
    def find_exact_match(
        self, 
        platform: str, 
        identifier: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find exact match for given platform and identifier
        
        Returns: 
            Dictionary with profile info if match found, None otherwise
        """
        # Normalize identifier based on platform
        normalized_id = self._normalize_identifier(platform, identifier)
        
        if not normalized_id:
            return None
        
        try:
            # Query platform_identities table
            response = self.db.table('platform_identities') \
                .select('*, unified_profiles(*)') \
                .eq('platform', platform) \
                .eq('identifier', normalized_id) \
                .execute()
            
            if response.data and len(response.data) > 0:
                identity = response.data[0]
                return {
                    'match_found': True,
                    'confidence': 1.0,
                    'match_type': 'deterministic',
                    'profile_id': identity.get('profile_id'),
                    'profile_name': identity.get('unified_profiles', {}).get('canonical_name'),
                    'matched_identity': identity
                }
        
        except Exception as e:
            print(f"Error in exact match: {str(e)}")
        
        return None
    
    def find_cross_platform_matches(
        self,
        identifiers: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """
        Find matches across multiple platforms
        
        Args:
            identifiers: Dict like {'email': 'sara@xyz.com', 'phone': '+91...'}
        
        Returns:
            List of potential matches with confidence scores
        """
        matches = []
        profile_ids = set()
        
        for platform, identifier in identifiers.items():
            match = self.find_exact_match(platform, identifier)
            if match and match['profile_id']:
                profile_id = match['profile_id']
                if profile_id not in profile_ids:
                    profile_ids.add(profile_id)
                    matches.append(match)
        
        return matches
    
    def _normalize_identifier(self, platform: str, identifier: str) -> Optional[str]:
        """Normalize identifier based on platform type"""
        if platform == 'email':
            return normalize_email(identifier)
        elif platform == 'whatsapp':
            return normalize_phone(identifier)
        elif platform in ['dashboard', 'instagram']:
            return normalize_username(identifier)
        
        return identifier.strip().lower() if identifier else None
    
    def create_match_candidate(
        self,
        source_identity_id: int,
        target_profile_id: int,
        match_details: Dict[str, Any]
    ) -> Optional[int]:
        """
        Create a match candidate record for manual review
        
        Returns: candidate_id if successful
        """
        try:
            response = self.db.table('match_candidates').insert({
                'source_identity_id': source_identity_id,
                'target_profile_id': target_profile_id,
                'match_type': 'deterministic',
                'confidence_score': 1.0,
                'match_details': match_details,
                'status': 'pending'
            }).execute()
            
            if response.data:
                return response.data[0]['id']
        
        except Exception as e:
            print(f"Error creating match candidate: {str(e)}")
        
        return None
