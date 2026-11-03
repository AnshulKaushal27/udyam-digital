import React from 'react';
import type { EmailJob } from '../types';
import { Send, CheckCircle2, XCircle, ExternalLink, Mail } from 'lucide-react';

interface SentTableProps {
  emails: EmailJob[];
  loading: boolean;
}

export const SentTable: React.FC<SentTableProps> = ({ emails, loading }) => {
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
        <div className="w-12 h-12 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 mx-auto flex items-center justify-center mb-3">
          <Send className="w-6 h-6" />
        </div>
        <h3 className="text-base font-semibold text-white mb-1">No Sent Emails Yet</h3>
        <p className="text-sm text-slate-400 max-w-sm mx-auto">
          As BullMQ workers process your scheduled email jobs via Ethereal SMTP, they will appear here with live preview links!
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
              <th className="py-3 px-4">Sent Time</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4 text-right">Ethereal Preview</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {emails.map((job) => {
              const isSent = job.status === 'SENT';
              const dateFormatted = job.sentAt ? new Date(job.sentAt).toLocaleString() : 'N/A';

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

                  {/* Sent Time */}
                  <td className="py-3.5 px-4 text-slate-300">
                    <span>{dateFormatted}</span>
                  </td>

                  {/* Status */}
                  <td className="py-3.5 px-4">
                    {isSent ? (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        <CheckCircle2 className="w-3 h-3" />
                        Sent
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-red-500/10 text-red-400 border border-red-500/20" title={job.errorMessage || 'Failed'}>
                        <XCircle className="w-3 h-3" />
                        Failed
                      </span>
                    )}
                  </td>

                  {/* Ethereal Preview Link */}
                  <td className="py-3.5 px-4 text-right">
                    {job.etherealUrl ? (
                      <a
                        href={job.etherealUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-[11px] font-medium text-blue-400 hover:text-blue-300 bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/20 px-2.5 py-1 rounded transition"
                      >
                        <span>View Email</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <span className="text-slate-500 text-[11px]">—</span>
                    )}
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
