"""
Phase 3: LLM Semantic Matching with Ollama Gemma 2B
"""
from typing import Optional, Dict, Any
import json
import ollama  # Ollama Python client

class LlmMatcher:
    """
    Uses Ollama Gemma 2B to semantically match two identities.
    """

    def __init__(self):
        self.model_name = 'gemma2:2b'

    def llm_match(self, identity1: Dict[str, Any], identity2: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Calls LLM with prompt and parses JSON response.

        `identity1` and `identity2` are dicts with keys such as:
        - platform, identifier, display_name
        """

        prompt = f"""
        Determine if these two identities represent the same person.

        Identity 1:
        - Platform: {identity1.get('platform', 'N/A')}
        - Identifier: {identity1.get('identifier', 'N/A')}
        - Name: {identity1.get('display_name', 'N/A')}

        Identity 2:
        - Platform: {identity2.get('platform', 'N/A')}
        - Identifier: {identity2.get('identifier', 'N/A')}
        - Name: {identity2.get('display_name', 'N/A')}

        Respond ONLY with a JSON containing keys:
        {{
          "is_match": true or false,
          "confidence": float between 0.0 and 1.0,
          "reasoning": "detailed explanation"
        }}
        """

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            # Parse JSON from LLM text response
            json_str = response.get('response', '{}')

            # Defensive: extract first { ... } substring in case of extra text
            start = json_str.find('{')
            end = json_str.rfind('}') + 1
            json_clean = json_str[start:end] if start != -1 and end != -1 else '{}'

            result = json.loads(json_clean)

            # Validate required keys
            is_match = result.get('is_match', False)
            confidence = float(result.get('confidence', 0.0))
            reasoning = result.get('reasoning', '')

            return {
                'is_match': is_match,
                'confidence': confidence,
                'reasoning': reasoning
            }
        except Exception as e:
            print(f"LLM error or malformed response: {str(e)}")
            return None
