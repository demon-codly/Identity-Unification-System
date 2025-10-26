import { useState, useEffect } from 'react';
import { apiService } from './services/api';
import { PLATFORMS } from './config';
import ProfileList from './components/ProfileList';
import AddIdentityForm from './components/AddIdentityForm';
import MatchingTool from './components/MatchingTool';
import StatsCard from './components/StatsCard';

function App() {
  const [activeTab, setActiveTab] = useState('profiles');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await apiService.getStats();
      if (response.success) {
        setStats(response.data);
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Identity Unification System
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      {stats && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <StatsCard
              title="Total Profiles"
              value={stats.total_profiles}
              icon="👥"
              color="blue"
            />
            <StatsCard
              title="Platform Identities"
              value={stats.total_identities}
              icon="🔗"
              color="green"
            />
            <StatsCard
              title="Pending Reviews"
              value={stats.pending_reviews}
              icon="⏳"
              color="yellow"
            />
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'profiles', label: 'Profiles', icon: '👥' },
              { id: 'add-identity', label: 'Add Identity', icon: '➕' },
              { id: 'matching', label: 'Find Matches', icon: '🔍' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                  ${activeTab === tab.id
                    ? 'border-primary text-primary'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'profiles' && <ProfileList onUpdate={loadStats} />}
        {activeTab === 'add-identity' && <AddIdentityForm onSuccess={loadStats} />}
        {activeTab === 'matching' && <MatchingTool />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            Built with Flask, React, Supabase & Ollama Gemma 2B
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
