import { useState } from 'react';
import { apiService } from '../services/api';
import { PLATFORMS } from '../config';

const AddIdentityForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    platform: 'email',
    identifier: '',
    display_name: '',
    auto_match: true,
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiService.addIdentity(formData);
      setResult(response);
      if (onSuccess) onSuccess();
      
      // Reset form
      setFormData({
        platform: 'email',
        identifier: '',
        display_name: '',
        auto_match: true,
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Add New Platform Identity
        </h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Platform Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Platform
            </label>
            <select
              name="platform"
              value={formData.platform}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              required
            >
              {PLATFORMS.map(platform => (
                <option key={platform.value} value={platform.value}>
                  {platform.icon} {platform.label}
                </option>
              ))}
            </select>
          </div>

          {/* Identifier */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Identifier *
            </label>
            <input
              type="text"
              name="identifier"
              value={formData.identifier}
              onChange={handleChange}
              placeholder={
                formData.platform === 'email' ? 'user@example.com' :
                formData.platform === 'whatsapp' ? '+919876543210' :
                formData.platform === 'instagram' ? '@username' :
                'username'
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              required
            />
          </div>

          {/* Display Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Display Name
            </label>
            <input
              type="text"
              name="display_name"
              value={formData.display_name}
              onChange={handleChange}
              placeholder="Full Name"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Auto Match */}
          <div className="flex items-center">
            <input
              type="checkbox"
              name="auto_match"
              checked={formData.auto_match}
              onChange={handleChange}
              className="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            />
            <label className="ml-2 block text-sm text-gray-700">
              Automatically find and link to existing profile
            </label>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-white py-3 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
          >
            {loading ? 'Adding...' : 'Add Identity'}
          </button>
        </form>

        {/* Success Message */}
        {result && result.success && (
          <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
            <h3 className="text-green-800 font-medium mb-2">✓ Success!</h3>
            <p className="text-sm text-green-700">
              Identity added successfully
              {result.match_result && (
                <span className="block mt-1">
                  Matched to profile: <strong>{result.match_result.profile_name}</strong>
                </span>
              )}
              {result.new_profile_created && (
                <span className="block mt-1">
                  New profile created
                </span>
              )}
            </p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <h3 className="text-red-800 font-medium mb-2">✗ Error</h3>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AddIdentityForm;
