import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { slackApi } from '../services/api';
import { X, MessageSquare, CheckCircle, Bell, AlertCircle, Link2, Unlink } from 'lucide-react';

interface SlackModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const SlackModal: React.FC<SlackModalProps> = ({ isOpen, onClose }) => {
  const { user, refreshProfile } = useAuth();
  const [webhookUrl, setWebhookUrl] = useState(user?.slackConfig?.webhookUrl || '');
  const [channel, setChannel] = useState(user?.slackConfig?.channel || '#general');
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  if (!isOpen) return null;

  const isConnected = user?.slackConfig?.isConnected;

  const handleOAuthConnect = async () => {
    setIsLoading(true);
    setStatusMessage(null);
    try {
      const url = await slackApi.getAuthorizeUrl();
      window.location.href = url;
    } catch (err: any) {
      setStatusMessage({
        type: 'error',
        text: err.response?.data?.error || err.message || 'Failed to start Slack OAuth',
      });
      setIsLoading(false);
    }
  };

  const handleSaveWebhook = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setStatusMessage(null);
    try {
      await slackApi.saveWebhook(webhookUrl, channel);
      await refreshProfile();
      setStatusMessage({
        type: 'success',
        text: 'Slack webhook saved and connected successfully!',
      });
    } catch (err: any) {
      setStatusMessage({
        type: 'error',
        text: err.response?.data?.error || err.message || 'Failed to save webhook',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendTest = async () => {
    setIsLoading(true);
    setStatusMessage(null);
    try {
      const res = await slackApi.sendTestNotification();
      setStatusMessage({
        type: 'success',
        text: res.message || 'Test message sent to Slack!',
      });
    } catch (err: any) {
      setStatusMessage({
        type: 'error',
        text: err.response?.data?.message || err.message || 'Failed to send test notification',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async () => {
    setIsLoading(true);
    setStatusMessage(null);
    try {
      await slackApi.disconnect();
      await refreshProfile();
      setWebhookUrl('');
      setStatusMessage({
        type: 'success',
        text: 'Slack integration disconnected.',
      });
    } catch (err: any) {
      setStatusMessage({
        type: 'error',
        text: 'Failed to disconnect Slack',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-800/40">
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <MessageSquare className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-white">Slack Notifications Integration</h2>
              <p className="text-xs text-slate-400">Get live alerts when a sender hits the hourly rate limit</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-5">
          {statusMessage && (
            <div
              className={`p-3 rounded-xl flex items-start gap-2.5 text-xs ${
                statusMessage.type === 'success'
                  ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-300'
                  : 'bg-red-500/10 border border-red-500/30 text-red-300'
              }`}
            >
              {statusMessage.type === 'success' ? (
                <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              ) : (
                <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
              )}
              <span>{statusMessage.text}</span>
            </div>
          )}

          {/* Connection Status Card */}
          <div className="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div
                className={`w-3 h-3 rounded-full ${
                  isConnected ? 'bg-emerald-400 shadow-sm shadow-emerald-400' : 'bg-slate-500'
                }`}
              />
              <div>
                <p className="text-xs font-semibold text-white">
                  {isConnected ? 'Connected to Slack' : 'Slack Not Connected'}
                </p>
                <p className="text-[11px] text-slate-400">
                  {isConnected
                    ? `Posting alerts to: ${user?.slackConfig?.channel || '#alerts'}`
                    : 'Connect to receive instant rate-limit warnings'}
                </p>
              </div>
            </div>

            {isConnected && (
              <button
                onClick={handleDisconnect}
                disabled={isLoading}
                className="flex items-center gap-1 text-[11px] font-medium text-red-400 hover:text-red-300 bg-red-500/10 hover:bg-red-500/20 px-2.5 py-1 rounded transition"
              >
                <Unlink className="w-3 h-3" />
                <span>Disconnect</span>
              </button>
            )}
          </div>

          {/* Option A: OAuth Flow */}
          <div className="space-y-2">
            <p className="text-xs font-semibold text-slate-300">Method 1: Connect via Slack OAuth</p>
            <button
              onClick={handleOAuthConnect}
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl text-xs font-semibold text-white transition"
            >
              <Link2 className="w-4 h-4 text-emerald-400" />
              <span>Authorize with Slack OAuth</span>
            </button>
          </div>

          <div className="relative flex py-1 items-center">
            <div className="flex-grow border-t border-slate-800"></div>
            <span className="flex-shrink mx-3 text-[10px] text-slate-500 uppercase tracking-widest">Or direct webhook</span>
            <div className="flex-grow border-t border-slate-800"></div>
          </div>

          {/* Option B: Direct Incoming Webhook */}
          <form onSubmit={handleSaveWebhook} className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Incoming Webhook URL
              </label>
              <input
                type="url"
                required
                value={webhookUrl}
                onChange={(e) => setWebhookUrl(e.target.value)}
                placeholder="https://hooks.slack.com/services/..."
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Channel Label</label>
              <input
                type="text"
                value={channel}
                onChange={(e) => setChannel(e.target.value)}
                placeholder="#general or #rate-limit-alerts"
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !webhookUrl}
              className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-xs font-semibold text-white rounded-lg transition"
            >
              Save Webhook
            </button>
          </form>

          {/* Send Test Notification Button */}
          {isConnected && (
            <div className="pt-2 border-t border-slate-800">
              <button
                type="button"
                onClick={handleSendTest}
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-2 py-2 px-3 bg-blue-600/10 hover:bg-blue-600/20 text-blue-400 border border-blue-500/20 rounded-lg text-xs font-medium transition"
              >
                <Bell className="w-3.5 h-3.5" />
                <span>Send Live Test Notification to Slack</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
