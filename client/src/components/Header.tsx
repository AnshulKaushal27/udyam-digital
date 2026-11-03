import React from 'react';
import { useAuth } from '../context/AuthContext';
import { LogOut, ExternalLink, Activity, MessageSquare } from 'lucide-react';

interface HeaderProps {
  onOpenSlackModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onOpenSlackModal }) => {
  const { user, logout } = useAuth();
  const isSlackConnected = user?.slackConfig?.isConnected;

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <span className="text-white font-bold text-lg tracking-wider">R</span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-white text-base tracking-tight">ReachInbox</span>
              <span className="text-[10px] font-semibold uppercase tracking-widest bg-blue-500/10 text-blue-400 border border-blue-500/20 px-1.5 py-0.5 rounded">
                Scheduler
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">Production-Grade Email Job Engine</p>
          </div>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-3 sm:gap-4">
          {/* Live Bull-Board link */}
          <a
            href="/admin/queues"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700/80 border border-slate-700 px-3 py-1.5 rounded-lg transition"
            title="Open Live BullMQ Queue Dashboard"
          >
            <Activity className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
            <span className="hidden md:inline">Bull-Board Live Queue</span>
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>

          {/* Slack Connection Button */}
          <button
            onClick={onOpenSlackModal}
            className={`flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-lg border transition ${
              isSlackConnected
                ? 'bg-emerald-950/40 border-emerald-500/30 text-emerald-300 hover:bg-emerald-950/60'
                : 'bg-slate-800 border-slate-700 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5 text-emerald-400" />
            <span className="hidden sm:inline">
              {isSlackConnected ? 'Slack: Connected' : 'Connect Slack'}
            </span>
            <span
              className={`w-2 h-2 rounded-full ${
                isSlackConnected ? 'bg-emerald-400 shadow-sm shadow-emerald-400' : 'bg-slate-500'
              }`}
            />
          </button>

          {/* User Profile */}
          {user && (
            <div className="flex items-center gap-3 pl-2 border-l border-slate-800">
              <div className="flex items-center gap-2.5">
                {user.avatarUrl ? (
                  <img
                    src={user.avatarUrl}
                    alt={user.name}
                    className="w-8 h-8 rounded-full border border-slate-700 object-cover"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold text-xs">
                    {user.name.charAt(0).toUpperCase()}
                  </div>
                )}
                <div className="hidden lg:block text-left">
                  <p className="text-xs font-medium text-slate-200 leading-tight">{user.name}</p>
                  <p className="text-[11px] text-slate-400 leading-tight truncate max-w-[140px]">{user.email}</p>
                </div>
              </div>

              {/* Logout */}
              <button
                onClick={logout}
                title="Logout"
                className="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
