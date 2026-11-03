import React, { useState, useEffect, useCallback } from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Header } from './components/Header';
import { StatsCards } from './components/StatsCards';
import { SearchBar } from './components/SearchBar';
import { ScheduledTable } from './components/ScheduledTable';
import { SentTable } from './components/SentTable';
import { ComposeModal } from './components/ComposeModal';
import { SlackModal } from './components/SlackModal';
import { LoginView } from './components/LoginView';
import { emailApi } from './services/api';
import type { EmailJob, EmailStats } from './types';
import { Plus, RefreshCw, Clock, Send, CheckCircle2 } from 'lucide-react';

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || 'dummy-google-client-id.apps.googleusercontent.com';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<'scheduled' | 'sent'>('scheduled');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchSource, setSearchSource] = useState('elasticsearch');

  const [scheduledEmails, setScheduledEmails] = useState<EmailJob[]>([]);
  const [sentEmails, setSentEmails] = useState<EmailJob[]>([]);
  const [stats, setStats] = useState<EmailStats | null>(null);

  const [loadingScheduled, setLoadingScheduled] = useState(false);
  const [loadingSent, setLoadingSent] = useState(false);
  const [loadingStats, setLoadingStats] = useState(false);

  const [isComposeOpen, setIsComposeOpen] = useState(false);
  const [isSlackOpen, setIsSlackOpen] = useState(false);
  const [bannerNotice, setBannerNotice] = useState<string | null>(null);

  // Check URL parameters for Slack OAuth return
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('slack_connected') === 'true') {
      setBannerNotice('🎉 Slack successfully connected! You will receive live alerts on rate-limit hits.');
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (params.get('slack_error')) {
      setBannerNotice(`⚠️ Slack connection error: ${params.get('slack_error')}`);
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const fetchStats = useCallback(async () => {
    setLoadingStats(true);
    try {
      const data = await emailApi.getEmailStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load stats:', err);
    } finally {
      setLoadingStats(false);
    }
  }, []);

  const fetchScheduled = useCallback(async () => {
    setLoadingScheduled(true);
    try {
      const res = await emailApi.getScheduledEmails(searchQuery);
      setScheduledEmails(res.data);
      setSearchSource(res.source);
    } catch (err) {
      console.error('Failed to load scheduled emails:', err);
    } finally {
      setLoadingScheduled(false);
    }
  }, [searchQuery]);

  const fetchSent = useCallback(async () => {
    setLoadingSent(true);
    try {
      const res = await emailApi.getSentEmails(searchQuery);
      setSentEmails(res.data);
      setSearchSource(res.source);
    } catch (err) {
      console.error('Failed to load sent emails:', err);
    } finally {
      setLoadingSent(false);
    }
  }, [searchQuery]);

  const handleRefresh = useCallback(() => {
    fetchStats();
    if (activeTab === 'scheduled') {
      fetchScheduled();
    } else {
      fetchSent();
    }
  }, [activeTab, fetchStats, fetchScheduled, fetchSent]);

  // Periodic polling for live updates
  useEffect(() => {
    handleRefresh();
    const interval = setInterval(handleRefresh, 4000);
    return () => clearInterval(interval);
  }, [handleRefresh]);

  if (!user) {
    return <LoginView />;
  }

  return (
    <div className="min-h-screen bg-[#0b0f19] text-slate-100 flex flex-col">
      <Header onOpenSlackModal={() => setIsSlackOpen(true)} />

      {/* Banner Notice */}
      {bannerNotice && (
        <div className="bg-blue-600/15 border-b border-blue-500/30 px-4 py-2.5 text-xs text-blue-300 flex items-center justify-between">
          <div className="flex items-center gap-2 max-w-7xl mx-auto w-full">
            <CheckCircle2 className="w-4 h-4 text-blue-400 shrink-0" />
            <span>{bannerNotice}</span>
          </div>
          <button onClick={() => setBannerNotice(null)} className="text-blue-300 hover:text-white">
            &times;
          </button>
        </div>
      )}

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Top Action Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">Email Job Scheduler</h1>
            <p className="text-xs text-slate-400 mt-1">
              Persistent BullMQ queue with Redis-backed rate limiting & Ethereal SMTP
            </p>
          </div>

          <div className="flex items-center gap-2.5">
            <button
              onClick={handleRefresh}
              title="Refresh Queue Data"
              className="p-2.5 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white rounded-xl transition"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
            <button
              onClick={() => setIsComposeOpen(true)}
              className="flex items-center gap-2 px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-blue-500/20 transition"
            >
              <Plus className="w-4 h-4" />
              <span>Compose New Email</span>
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <StatsCards stats={stats} loading={loadingStats} />

        {/* Tab Selection & Search */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-2">
          {/* Tabs */}
          <div className="flex items-center p-1 bg-slate-900 border border-slate-800 rounded-xl">
            <button
              onClick={() => setActiveTab('scheduled')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-medium transition ${
                activeTab === 'scheduled'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Clock className="w-3.5 h-3.5" />
              <span>Scheduled Emails</span>
              <span className={`px-1.5 py-0.2 rounded-full text-[10px] ${
                activeTab === 'scheduled' ? 'bg-blue-700 text-blue-100' : 'bg-slate-800 text-slate-400'
              }`}>
                {(stats?.scheduled ?? 0) + (stats?.delayed ?? 0)}
              </span>
            </button>

            <button
              onClick={() => setActiveTab('sent')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-medium transition ${
                activeTab === 'sent'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Send className="w-3.5 h-3.5" />
              <span>Sent Emails</span>
              <span className={`px-1.5 py-0.2 rounded-full text-[10px] ${
                activeTab === 'sent' ? 'bg-blue-700 text-blue-100' : 'bg-slate-800 text-slate-400'
              }`}>
                {stats?.sent ?? 0}
              </span>
            </button>
          </div>

          {/* Search Bar */}
          <div className="w-full sm:max-w-md">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              source={searchSource}
              placeholder={`Search ${activeTab === 'scheduled' ? 'scheduled' : 'sent'} emails...`}
            />
          </div>
        </div>

        {/* Table View */}
        {activeTab === 'scheduled' ? (
          <ScheduledTable
            emails={scheduledEmails}
            loading={loadingScheduled}
            onRefresh={fetchScheduled}
          />
        ) : (
          <SentTable emails={sentEmails} loading={loadingSent} />
        )}
      </main>

      {/* Modals */}
      <ComposeModal
        isOpen={isComposeOpen}
        onClose={() => setIsComposeOpen(false)}
        onSuccess={() => {
          handleRefresh();
          setActiveTab('scheduled');
        }}
      />

      <SlackModal isOpen={isSlackOpen} onClose={() => setIsSlackOpen(false)} />
    </div>
  );
};

export default function App() {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <Dashboard />
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}
