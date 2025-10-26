"""
REST API Routes for Identity Unification System
Phase 1: Deterministic Matching
"""
from flask import Blueprint, request, jsonify
from app.database import get_db
from app.matching.deterministic import DeterministicMatcher
from app.utils.normalizers import normalize_email, normalize_phone, normalize_name
from app.utils.validators import validate_identity_data
from app.matching.fuzzy_matcher import FuzzyMatcher
from app.matching.llm_matcher import LlmMatcher

llm_matcher = LlmMatcher()
matcher = DeterministicMatcher()
fuzzy_matcher = FuzzyMatcher()
api_bp = Blueprint('api', __name__)
db = get_db()
matcher = DeterministicMatcher()


# ==================== Health Check ====================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Identity Unification API',
        'version': '1.0.0',
        'phase': 'Phase 1 - Deterministic Matching'
    }), 200


# ==================== Profiles ====================

@api_bp.route('/profiles', methods=['GET'])
def get_profiles():
    """Get all unified profiles"""
    try:
        response = db.table('unified_profiles') \
            .select('*, platform_identities(*)') \
            .eq('status', 'active') \
            .execute()
        
        return jsonify({
            'success': True,
            'data': response.data,
            'count': len(response.data)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    """Get specific profile with all linked identities"""
    try:
        # Get profile
        profile_response = db.table('unified_profiles') \
            .select('*') \
            .eq('id', profile_id) \
            .execute()
        
        if not profile_response.data:
            return jsonify({
                'success': False,
                'error': 'Profile not found'
            }), 404
        
        # Get linked identities
        identities_response = db.table('platform_identities') \
            .select('*') \
            .eq('profile_id', profile_id) \
            .execute()
        
        profile = profile_response.data[0]
        profile['identities'] = identities_response.data
        
        return jsonify({
            'success': True,
            'data': profile
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/profiles', methods=['POST'])
def create_profile():
    """Create new unified profile"""
    try:
        data = request.get_json()
        
        if not data.get('canonical_name'):
            return jsonify({
                'success': False,
                'error': 'canonical_name is required'
            }), 400
        
        # Normalize name
        canonical_name = normalize_name(data['canonical_name'])
        
        response = db.table('unified_profiles').insert({
            'canonical_name': canonical_name,
            'status': 'active'
        }).execute()
        
        return jsonify({
            'success': True,
            'data': response.data[0]
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== Identities ====================

@api_bp.route('/identities', methods=['GET'])
def get_identities():
    """Get all platform identities"""
    try:
        response = db.table('platform_identities') \
            .select('*, unified_profiles(canonical_name)') \
            .execute()
        
        return jsonify({
            'success': True,
            'data': response.data,
            'count': len(response.data)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/identities', methods=['POST'])
def add_identity():
    """
    Add new platform identity
    
    Request body:
    {
        "platform": "email",
        "identifier": "sara.johnson@xyz.com",
        "display_name": "Sara Johnson",
        "auto_match": true  # Optional: automatically find and link to profile
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, errors = validate_identity_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        platform = data['platform']
        identifier = data['identifier']
        display_name = data.get('display_name', '')
        auto_match = data.get('auto_match', True)
        
        # Check if identity already exists
        existing = db.table('platform_identities') \
            .select('*') \
            .eq('platform', platform) \
            .eq('identifier', identifier) \
            .execute()
        
        if existing.data:
            return jsonify({
                'success': False,
                'error': 'Identity already exists',
                'existing_identity': existing.data[0]
            }), 409
        
        profile_id = None
        match_result = None
        
        # Try to find exact match if auto_match is enabled
        if auto_match:
            match_result = matcher.find_exact_match(platform, identifier)
            if match_result and match_result['profile_id']:
                profile_id = match_result['profile_id']
        
        # If no match found and display_name provided, create new profile
        if not profile_id and display_name:
            normalized_name = normalize_name(display_name)
            profile_response = db.table('unified_profiles').insert({
                'canonical_name': normalized_name,
                'status': 'active'
            }).execute()
            profile_id = profile_response.data[0]['id']
        
        # Create identity
        identity_response = db.table('platform_identities').insert({
            'profile_id': profile_id,
            'platform': platform,
            'identifier': identifier,
            'display_name': display_name,
            'confidence_score': 1.0 if match_result else 0.0,
            'verified': bool(match_result)
        }).execute()
        
        return jsonify({
            'success': True,
            'data': identity_response.data[0],
            'match_result': match_result,
            'new_profile_created': profile_id is not None and not match_result
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== Matching ====================

@api_bp.route('/match', methods=['POST'])
def find_matches():
    try:
        data = request.get_json()
        if not data.get('identifiers'):
            return jsonify({
                'success': False,
                'error': 'identifiers object is required'
            }), 400

        identifiers = data['identifiers']
        matches = []

        # 1. Deterministic matching (stop/search here if found)
        for platform, identifier in identifiers.items():
            if not isinstance(identifier, str):
                continue
            result = matcher.find_exact_match(platform, identifier)
            if result:
                matches.append(result)

        if matches:
            # Deterministic match found, return immediately
            return jsonify({
                'success': True,
                'matches': matches,
                'match_count': len(matches)
            }), 200

        # 2. Fuzzy matching (only if *no* deterministic match)
        first_platform = None
        first_id = None
        for p, ident in identifiers.items():
            if isinstance(ident, str):
                first_platform = p
                first_id = ident
                break

        if first_platform and first_id:
            display_name = data.get('display_name')
            if not isinstance(display_name, str):
                display_name = None

            fuzzy_results = fuzzy_matcher.find_fuzzy_matches(
                first_platform, first_id, display_name
            )

            if fuzzy_results:
                # Fuzzy match found, return immediately
                return jsonify({
                    'success': True,
                    'matches': fuzzy_results,
                    'match_count': len(fuzzy_results)
                }), 200

        # 3. LLM matching (only if *no* deterministic or fuzzy match)
        low_confidence_threshold = 0.65
        # Use first identifier vs all profiles for LLM comparison
        if first_platform and first_id:
            first_name = data.get('display_name') if isinstance(data.get('display_name'), str) else None
            db_client = get_db()
            profiles_resp = db_client.table('platform_identities')\
                .select('*, unified_profiles(canonical_name)')\
                .execute()
            candidates = profiles_resp.data if profiles_resp.data else []
            for identity in candidates:
                identity_data = {
                    'platform': identity.get('platform'),
                    'identifier': identity.get('identifier'),
                    'display_name': identity.get('display_name') or identity.get('unified_profiles', {}).get('canonical_name')
                }
                source_identity = {
                    'platform': first_platform,
                    'identifier': first_id,
                    'display_name': first_name
                }
                llm_result = llm_matcher.llm_match(source_identity, identity_data)
                if llm_result and llm_result['is_match'] and llm_result['confidence'] >= low_confidence_threshold:
                    matches.append({
                        'profile_id': identity.get('profile_id'),
                        'profile_name': identity.get('unified_profiles', {}).get('canonical_name'),
                        'matched_identity': identity,
                        'confidence': round(llm_result['confidence'], 2),
                        'match_type': 'llm',
                        'reasoning': llm_result.get('reasoning', '')
                    })
            if matches:
                return jsonify({
                    'success': True,
                    'matches': matches,
                    'match_count': len(matches)
                }), 200

        # No match of any kind
        return jsonify({
            'success': True,
            'matches': [],
            'match_count': 0
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500




# ==================== Match Candidates (Manual Review) ====================

@api_bp.route('/candidates', methods=['GET'])
def get_candidates():
    """Get all pending match candidates for review"""
    try:
        status = request.args.get('status', 'pending')
        
        response = db.table('match_candidates') \
            .select('*, platform_identities(*), unified_profiles(*)') \
            .eq('status', status) \
            .order('created_at', desc=True) \
            .execute()
        
        return jsonify({
            'success': True,
            'data': response.data,
            'count': len(response.data)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/candidates/<int:candidate_id>/approve', methods=['POST'])
def approve_candidate(candidate_id):
    """Approve a match candidate"""
    try:
        data = request.get_json() or {}
        reviewed_by = data.get('reviewed_by', 'admin')
        
        response = db.table('match_candidates') \
            .update({
                'status': 'approved',
                'reviewed_by': reviewed_by,
                'reviewed_at': 'now()'
            }) \
            .eq('id', candidate_id) \
            .execute()
        
        return jsonify({
            'success': True,
            'data': response.data[0] if response.data else None
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/candidates/<int:candidate_id>/reject', methods=['POST'])
def reject_candidate(candidate_id):
    """Reject a match candidate"""
    try:
        data = request.get_json() or {}
        reviewed_by = data.get('reviewed_by', 'admin')
        
        response = db.table('match_candidates') \
            .update({
                'status': 'rejected',
                'reviewed_by': reviewed_by,
                'reviewed_at': 'now()'
            }) \
            .eq('id', candidate_id) \
            .execute()
        
        return jsonify({
            'success': True,
            'data': response.data[0] if response.data else None
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== Statistics ====================

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        profiles_count = db.table('unified_profiles') \
            .select('*', count='exact') \
            .eq('status', 'active') \
            .execute()
        
        identities_count = db.table('platform_identities') \
            .select('*', count='exact') \
            .execute()
        
        pending_candidates = db.table('match_candidates') \
            .select('*', count='exact') \
            .eq('status', 'pending') \
            .execute()
        
        return jsonify({
            'success': True,
            'data': {
                'total_profiles': profiles_count.count,
                'total_identities': identities_count.count,
                'pending_reviews': pending_candidates.count
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
