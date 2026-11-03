import React from 'react';
import type { EmailStats } from '../types';
import { Clock, Send, AlertTriangle, XCircle, Zap } from 'lucide-react';

interface StatsCardsProps {
  stats: EmailStats | null;
  loading: boolean;
}

export const StatsCards: React.FC<StatsCardsProps> = ({ stats, loading }) => {
  const cards = [
    {
      title: 'Scheduled Jobs',
      value: stats?.scheduled ?? 0,
      icon: Clock,
      color: 'text-blue-400',
      bg: 'bg-blue-500/10 border-blue-500/20',
      description: 'Queued in BullMQ',
    },
    {
      title: 'Rate-Limit Delayed',
      value: stats?.delayed ?? 0,
      icon: AlertTriangle,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10 border-amber-500/20',
      description: 'Pushed to next hour window',
    },
    {
      title: 'Successfully Sent',
      value: stats?.sent ?? 0,
      icon: Send,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10 border-emerald-500/20',
      description: 'Dispatched via Ethereal SMTP',
    },
    {
      title: 'Failed Sends',
      value: stats?.failed ?? 0,
      icon: XCircle,
      color: 'text-red-400',
      bg: 'bg-red-500/10 border-red-500/20',
      description: 'Bounce / Error occurred',
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, index) => {
        const Icon = card.icon;
        return (
          <div
            key={index}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 relative overflow-hidden transition hover:border-slate-700"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{card.title}</span>
              <div className={`p-2 rounded-lg border ${card.bg}`}>
                <Icon className={`w-4 h-4 ${card.color}`} />
              </div>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
                {loading ? (
                  <span className="inline-block w-8 h-7 bg-slate-800 rounded animate-pulse" />
                ) : (
                  card.value
                )}
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1 flex items-center gap-1">
              <Zap className="w-3 h-3 text-slate-400" />
              {card.description}
            </p>
          </div>
        );
      })}
    </div>
  );
};
