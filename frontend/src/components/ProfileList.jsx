import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { PLATFORMS } from '../config';

const ProfileList = ({ onUpdate }) => {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedProfile, setExpandedProfile] = useState(null);

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      setLoading(true);
      const response = await apiService.getProfiles();
      if (response.success) {
        setProfiles(response.data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getPlatformIcon = (platform) => {
    return PLATFORMS.find(p => p.value === platform)?.icon || '🔗';
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Error: {error}</p>
        <button
          onClick={loadProfiles}
          className="mt-2 text-sm text-red-600 hover:text-red-800"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Unified Profiles</h2>
        <button
          onClick={loadProfiles}
          className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          🔄 Refresh
        </button>
      </div>

      {profiles.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <p className="text-gray-500 text-lg">No profiles found</p>
          <p className="text-gray-400 text-sm mt-2">Add an identity to create your first profile</p>
        </div>
      ) : (
        <div className="space-y-4">
          {profiles.map((profile) => (
            <div
              key={profile.id}
              className="bg-white rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div
                className="p-6 cursor-pointer"
                onClick={() => setExpandedProfile(
                  expandedProfile === profile.id ? null : profile.id
                )}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {profile.canonical_name}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {profile.platform_identities?.length || 0} linked identities
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {profile.status}
                    </span>
                    <span className="text-gray-400">
                      {expandedProfile === profile.id ? '▲' : '▼'}
                    </span>
                  </div>
                </div>
              </div>

              {expandedProfile === profile.id && profile.platform_identities && (
                <div className="border-t border-gray-200 p-6 bg-gray-50">
                  <h4 className="text-sm font-medium text-gray-700 mb-4">
                    Linked Platform Identities
                  </h4>
                  <div className="space-y-3">
                    {profile.platform_identities.map((identity) => (
                      <div
                        key={identity.id}
                        className="flex items-center justify-between bg-white p-4 rounded-lg border border-gray-200"
                      >
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">
                            {getPlatformIcon(identity.platform)}
                          </span>
                          <div>
                            <p className="text-sm font-medium text-gray-900">
                              {identity.platform.charAt(0).toUpperCase() + identity.platform.slice(1)}
                            </p>
                            <p className="text-xs text-gray-500">
                              {identity.identifier}
                            </p>
                            {identity.display_name && (
                              <p className="text-xs text-gray-400 mt-1">
                                Display: {identity.display_name}
                              </p>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          {identity.verified && (
                            <span className="text-green-500 text-sm">✓ Verified</span>
                          )}
                          <span className="text-xs text-gray-500">
                            {(identity.confidence_score * 100).toFixed(0)}% confidence
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProfileList;
