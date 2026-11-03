import React from 'react';
import type { EmailJob } from '../types';
import { Clock, AlertTriangle, Mail } from 'lucide-react';

interface ScheduledTableProps {
  emails: EmailJob[];
  loading: boolean;
  onRefresh: () => void;
}

export const ScheduledTable: React.FC<ScheduledTableProps> = ({ emails, loading }) => {
  if (loading && emails.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 space-y-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-14 bg-slate-800/50 rounded-lg animate-pulse" />
        ))}
      </div>
    );
  }

  if (emails.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center">
        <div className="w-12 h-12 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 mx-auto flex items-center justify-center mb-3">
          <Clock className="w-6 h-6" />
        </div>
        <h3 className="text-base font-semibold text-white mb-1">No Scheduled Emails</h3>
        <p className="text-sm text-slate-400 max-w-sm mx-auto">
          You don't have any emails in the BullMQ queue right now. Click "Compose New Email" to schedule outreach!
        </p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-800/40 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              <th className="py-3 px-4">Recipient</th>
              <th className="py-3 px-4">Subject</th>
              <th className="py-3 px-4">Sender</th>
              <th className="py-3 px-4">Scheduled Time</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Rate Settings</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {emails.map((job) => {
              const isDelayed = job.status === 'DELAYED';
              const dateFormatted = new Date(job.scheduledAt).toLocaleString();

              return (
                <tr key={job.id} className="hover:bg-slate-800/30 transition">
                  {/* Recipient */}
                  <td className="py-3.5 px-4 font-medium text-slate-200">
                    <div className="flex items-center gap-2">
                      <Mail className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span className="truncate max-w-[200px]" title={job.recipientEmail}>
                        {job.recipientEmail}
                      </span>
                    </div>
                  </td>

                  {/* Subject */}
                  <td className="py-3.5 px-4 text-slate-300">
                    <span className="truncate block max-w-[240px]" title={job.subject}>
                      {job.subject}
                    </span>
                  </td>

                  {/* Sender */}
                  <td className="py-3.5 px-4 text-slate-400 font-mono text-[11px]">
                    <span className="truncate block max-w-[150px]" title={job.senderEmail}>
                      {job.senderEmail}
                    </span>
                  </td>

                  {/* Scheduled Time */}
                  <td className="py-3.5 px-4 text-slate-300">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3 h-3 text-slate-400" />
                      <span>{dateFormatted}</span>
                    </div>
                  </td>

                  {/* Status */}
                  <td className="py-3.5 px-4">
                    {isDelayed ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-amber-500/10 text-amber-300 border border-amber-500/20">
                        <AlertTriangle className="w-3 h-3" />
                        Delayed (Next Window)
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-blue-500/10 text-blue-300 border border-blue-500/20">
                        <Clock className="w-3 h-3" />
                        Scheduled
                      </span>
                    )}
                  </td>

                  {/* Settings */}
                  <td className="py-3.5 px-4 text-slate-400">
                    <span className="text-[10px] bg-slate-800 border border-slate-700/60 px-1.5 py-0.5 rounded">
                      Delay: {job.delayBetweenMs / 1000}s | Limit: {job.hourlyLimit}/hr
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
