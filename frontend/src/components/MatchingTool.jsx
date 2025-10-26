import { useState } from 'react';
import { apiService } from '../services/api';
import { PLATFORMS, CONFIDENCE_LEVELS } from '../config';

const MATCH_TYPE_COLORS = {
  deterministic: { border: 'border-green-400', bg: 'bg-green-50', hover: 'hover:bg-green-100', label: 'Deterministic', color: 'green' },
  fuzzy: { border: 'border-yellow-400', bg: 'bg-yellow-50', hover: 'hover:bg-yellow-100', label: 'Fuzzy', color: 'yellow' },
  llm: { border: 'border-purple-500', bg: 'bg-purple-50', hover: 'hover:bg-purple-100', label: 'LLM (Semantic)', color: 'purple' }
};

const MatchingTool = () => {
  const [identifiers, setIdentifiers] = useState({});
  const [displayName, setDisplayName] = useState('');
  const [matches, setMatches] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expandedIdx, setExpandedIdx] = useState(null);

  const handleInputChange = (platform, value) => {
    setIdentifiers(prev => {
      if (!value.trim()) {
        const { [platform]: _, ...rest } = prev;
        return rest;
      }
      return { ...prev, [platform]: value };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (Object.keys(identifiers).length === 0) {
      setError('Please enter at least one identifier');
      return;
    }

    setLoading(true);
    setError(null);
    setMatches(null);
    setExpandedIdx(null);

    try {
      const response = await apiService.findMatches({ identifiers, display_name: displayName });
      setMatches(response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceLevel = (score) => {
    if (score >= CONFIDENCE_LEVELS.HIGH.min) return { ...CONFIDENCE_LEVELS.HIGH };
    if (score >= CONFIDENCE_LEVELS.MEDIUM.min) return { ...CONFIDENCE_LEVELS.MEDIUM };
    return { ...CONFIDENCE_LEVELS.LOW };
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Find Cross-Platform Matches</h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <p className="text-sm text-gray-600 mb-4">
            Enter identifiers from different platforms to find if they belong to the same person.
          </p>

          {PLATFORMS.map(platform => (
            <div key={platform.value}>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {platform.icon} {platform.label}
              </label>
              <input
                type="text"
                value={identifiers[platform.value] || ''}
                onChange={e => handleInputChange(platform.value, e.target.value)}
                placeholder={
                  platform.value === 'email' ? 'user@example.com' :
                  platform.value === 'whatsapp' ? '+919876543210' :
                  platform.value === 'instagram' ? '@username' :
                  'username'
                }
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
          ))}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Display Name (Optional, helps fuzzy & semantic matching)
            </label>
            <input
              type="text"
              value={displayName}
              onChange={e => setDisplayName(e.target.value)}
              placeholder="Full Name"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          <button
            type="submit"
            disabled={loading || Object.keys(identifiers).length === 0}
            className="w-full bg-primary text-white py-3 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
          >
            {loading ? 'Searching...' : 'Find Matches'}
          </button>
        </form>

        {matches && (
          <div className="mt-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Match Results ({matches.match_count} found)
            </h3>

            {matches.match_count === 0 ? (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-800">No matches found.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {matches.matches.map((match, index) => {
                  const conf = getConfidenceLevel(match.confidence);
                  const matchTypeDetails = MATCH_TYPE_COLORS[match.match_type] || MATCH_TYPE_COLORS['fuzzy'];
                  return (
                    <div
                      key={index}
                      className={`border rounded-lg p-4 cursor-pointer ${matchTypeDetails.border} ${matchTypeDetails.bg} ${matchTypeDetails.hover}`}
                      onClick={() => setExpandedIdx(expandedIdx === index ? null : index)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-gray-900">{match.profile_name}</h4>
                        <span className={`text-xs px-2 py-1 rounded font-semibold text-${matchTypeDetails.color}-800 bg-${matchTypeDetails.color}-200`}>
                          {(match.confidence * 100).toFixed(0)}% Confidence ({matchTypeDetails.label})
                        </span>
                      </div>
                      <p className="text-sm text-gray-700">Profile ID: {match.profile_id}</p>

                      {match.match_type === 'llm' && expandedIdx === index && (
                        <div className="mt-3 p-3 bg-purple-100 border border-purple-300 rounded text-purple-900 whitespace-pre-wrap font-mono text-xs">
                          <strong>LLM Reasoning:</strong>
                          <br />
                          {match.reasoning || 'No explanation provided.'}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchingTool;
