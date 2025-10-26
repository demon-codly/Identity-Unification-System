/**
 * Application Configuration
 */

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api/v1';

export const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
export const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';

export const PLATFORMS = [
  { value: 'email', label: 'Email', icon: '📧' },
  { value: 'whatsapp', label: 'WhatsApp', icon: '📱' },
  { value: 'dashboard', label: 'Dashboard', icon: '🖥️' },
  { value: 'instagram', label: 'Instagram', icon: '📸' }
];

export const CONFIDENCE_LEVELS = {
  HIGH: { min: 0.85, color: 'green', label: 'High' },
  MEDIUM: { min: 0.65, color: 'yellow', label: 'Medium' },
  LOW: { min: 0, color: 'red', label: 'Low' }
};

