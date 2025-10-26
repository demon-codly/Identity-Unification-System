"""
Phase 2: Fuzzy Matching Logic using RapidFuzz and Phonetics
"""
from typing import Optional, Dict, Any, List
from rapidfuzz import fuzz
import phonetics

from app.utils.normalizers import normalize_name, normalize_username, normalize_email
from app.database import get_db


class FuzzyMatcher:
    """
    Implements approximate matching with fuzzy logic and phonetic comparison.
    Confidence score ranges from 0.65 to 0.95.
    """

    def __init__(self):
        self.db = get_db()

    def calculate_fuzzy_score(self, str1: str, str2: str) -> float:
        if not isinstance(str1, str) or not isinstance(str2, str):
            return 0.0
        if not str1 or not str2:
            return 0.0

        ratio = fuzz.ratio(str1, str2) / 100.0
        token_sort = fuzz.token_sort_ratio(str1, str2) / 100.0
        partial = fuzz.partial_ratio(str1, str2) / 100.0

        weighted_score = (0.5 * ratio) + (0.3 * token_sort) + (0.2 * partial)
        return weighted_score

    def phonetic_match_score(self, name1: str, name2: str) -> float:
        if not isinstance(name1, str) or not isinstance(name2, str):
            return 0.0
        if not name1 or not name2:
            return 0.0
        return 1.0 if phonetics.metaphone(name1) == phonetics.metaphone(name2) else 0.0

    def find_fuzzy_matches(
        self,
        platform: str,
        identifier: str,
        display_name: Optional[str] = None,
        threshold: float = 0.65,
    ) -> List[Dict[str, Any]]:
        if not isinstance(identifier, str):
            return []
        normalized_id = None
        if platform == "email":
            normalized_id = normalize_email(identifier)
        elif platform == "whatsapp":
            normalized_id = identifier  # phone normalization could be improved
        elif platform in ["dashboard", "instagram"]:
            normalized_id = normalize_username(identifier)
        else:
            normalized_id = identifier.lower() if identifier else None

        norm_display_name = normalize_name(display_name) if display_name else None

        if not normalized_id and not norm_display_name:
            return []

        try:
            response = (
                self.db.table("platform_identities")
                .select("*, unified_profiles(canonical_name)")
                .execute()
            )
            candidates = response.data if response.data else []

            results = []

            for identity in candidates:
                candidate_id = identity.get("identifier")
                candidate_name = (
                    identity.get("display_name")
                    or identity.get("unified_profiles", {}).get("canonical_name")
                )
                score_id = 0.0
                score_name = 0.0
                phon_score = 0.0

                if normalized_id and candidate_id and isinstance(candidate_id, str):
                    score_id = self.calculate_fuzzy_score(
                        normalized_id.lower(), candidate_id.lower()
                    )

                if norm_display_name and candidate_name and isinstance(candidate_name, str):
                    score_name = self.calculate_fuzzy_score(
                        norm_display_name.lower(), candidate_name.lower()
                    )
                    phon_score = self.phonetic_match_score(norm_display_name, candidate_name)

                weighted_score = 0.0
                weights = 0.0

                if score_id > 0:
                    weighted_score += 0.6 * score_id
                    weights += 0.6

                if score_name > 0:
                    weighted_score += 0.3 * score_name
                    weights += 0.3

                if phon_score > 0:
                    weighted_score += 0.1 * phon_score
                    weights += 0.1

                confidence = weighted_score / weights if weights > 0 else 0.0

                if confidence >= threshold:
                    results.append(
                        {
                            "profile_id": identity.get("profile_id"),
                            "profile_name": identity.get("unified_profiles", {}).get(
                                "canonical_name"
                            ),
                            "matched_identity": identity,
                            "confidence": round(confidence, 2),
                            "match_type": "fuzzy",
                        }
                    )

            results.sort(key=lambda x: x["confidence"], reverse=True)
            return results

        except Exception as e:
            print(f"Error in fuzzy match: {str(e)}")
            return []
