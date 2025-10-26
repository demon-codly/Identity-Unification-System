/**
 * API Service Layer
 */
import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here later
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const errorMessage = error.response?.data?.error || error.message || 'An error occurred';
    return Promise.reject(new Error(errorMessage));
  }
);

// API Methods
export const apiService = {
  // Health Check
  healthCheck: () => api.get('/health'),

  // Profiles
  getProfiles: () => api.get('/profiles'),
  getProfile: (id) => api.get(`/profiles/${id}`),
  createProfile: (data) => api.post('/profiles', data),

  // Identities
  getIdentities: () => api.get('/identities'),
  addIdentity: (data) => api.post('/identities', data),

  // Matching
  findMatches: (identifiers) => api.post('/match', { identifiers }),

  // Candidates
  getCandidates: (status = 'pending') => api.get(`/candidates?status=${status}`),
  approveCandidate: (id, reviewedBy = 'admin') => api.post(`/candidates/${id}/approve`, { reviewed_by: reviewedBy }),
  rejectCandidate: (id, reviewedBy = 'admin') => api.post(`/candidates/${id}/reject`, { reviewed_by: reviewedBy }),

  // Stats
  getStats: () => api.get('/stats'),
};

export default api;
