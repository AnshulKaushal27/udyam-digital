import React, { useState } from 'react';
import Papa from 'papaparse';
import { emailApi } from '../services/api';
import { X, Upload, Mail, Clock, ShieldAlert, Sparkles, AlertCircle } from 'lucide-react';

interface ComposeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const ComposeModal: React.FC<ComposeModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [senderEmail, setSenderEmail] = useState('growth@reachinbox.ai');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [recipientsText, setRecipientsText] = useState('');
  const [detectedEmails, setDetectedEmails] = useState<string[]>([]);
  const [startTime, setStartTime] = useState('');
  const [delayBetweenSeconds, setDelayBetweenSeconds] = useState(2);
  const [hourlyLimit, setHourlyLimit] = useState(50);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  // Extract valid emails from text or parsed CSV rows
  const extractEmails = (text: string): string[] => {
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
    const matches = text.match(emailRegex) || [];
    return Array.from(new Set(matches.map((e) => e.toLowerCase())));
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setErrorMessage(null);

    if (file.name.endsWith('.csv')) {
      Papa.parse(file, {
        complete: (results) => {
          const rawText = JSON.stringify(results.data);
          const found = extractEmails(rawText);
          setDetectedEmails(found);
          setRecipientsText(found.join('\n'));
        },
        error: (err) => {
          setErrorMessage('Failed to parse CSV file: ' + err.message);
        },
      });
    } else {
      // Plain text file
      const reader = new FileReader();
      reader.onload = (event) => {
        const text = event.target?.result as string;
        const found = extractEmails(text);
        setDetectedEmails(found);
        setRecipientsText(found.join('\n'));
      };
      reader.readAsText(file);
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    setRecipientsText(val);
    const found = extractEmails(val);
    setDetectedEmails(found);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    const emailList = detectedEmails.length > 0 ? detectedEmails : extractEmails(recipientsText);

    if (emailList.length === 0) {
      setErrorMessage('Please enter or upload at least one valid recipient email address.');
      return;
    }

    if (!subject.trim()) {
      setErrorMessage('Subject is required.');
      return;
    }

    if (!body.trim()) {
      setErrorMessage('Email body cannot be empty.');
      return;
    }

    setIsSubmitting(true);
    try {
      await emailApi.scheduleEmails({
        recipients: emailList,
        senderEmail,
        subject,
        body,
        startTime: startTime ? new Date(startTime).toISOString() : undefined,
        delayBetweenMs: Math.max(500, delayBetweenSeconds * 1000),
        hourlyLimit: Math.max(1, hourlyLimit),
      });

      onSuccess();
      onClose();
    } catch (err: any) {
      setErrorMessage(err.response?.data?.error || err.message || 'Failed to schedule emails');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm overflow-y-auto">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden my-8">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-800/40">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Mail className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-white">Compose & Schedule Email Campaign</h2>
              <p className="text-xs text-slate-400">Queue emails with BullMQ rate limiting and concurrency</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {errorMessage && (
            <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-xl flex items-start gap-2.5 text-xs text-red-300">
              <AlertCircle className="w-4 h-4 shrink-0 text-red-400 mt-0.5" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Sender Email */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Sender Email Address <span className="text-blue-400">*</span>
            </label>
            <input
              type="email"
              required
              value={senderEmail}
              onChange={(e) => setSenderEmail(e.target.value)}
              placeholder="e.g. outreach@reachinbox.ai"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Lead Upload (CSV / TXT) */}
          <div className="border border-dashed border-slate-700 rounded-xl p-4 bg-slate-800/30 text-center">
            <div className="flex flex-col items-center justify-center">
              <Upload className="w-6 h-6 text-blue-400 mb-2" />
              <label className="cursor-pointer text-xs font-semibold text-blue-400 hover:text-blue-300 transition">
                <span>Upload CSV or TXT lead file</span>
                <input
                  type="file"
                  accept=".csv,.txt"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
              <p className="text-[11px] text-slate-500 mt-1">
                Accepts spreadsheets or raw email lists. Lead count will be auto-calculated.
              </p>
            </div>

            {detectedEmails.length > 0 && (
              <div className="mt-3 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
                <Sparkles className="w-3.5 h-3.5" />
                <span>{detectedEmails.length} email addresses detected</span>
              </div>
            )}
          </div>

          {/* Recipients Textarea */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Recipients (or paste manually, separated by comma/newline)
            </label>
            <textarea
              rows={2}
              value={recipientsText}
              onChange={handleTextareaChange}
              placeholder="lead1@acme.com, lead2@startup.io..."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Subject */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Subject <span className="text-blue-400">*</span>
            </label>
            <input
              type="text"
              required
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. Quick question regarding your outreach workflow"
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Body */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">
              Email Body <span className="text-blue-400">*</span>
            </label>
            <textarea
              required
              rows={4}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="Write your email copy here..."
              className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Scheduling & Rate Limiting Controls */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-slate-800">
            {/* Start Time */}
            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1 flex items-center gap-1">
                <Clock className="w-3 h-3 text-slate-500" />
                Start Time (Optional)
              </label>
              <input
                type="datetime-local"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
              <span className="text-[10px] text-slate-500">Leave blank to start immediately</span>
            </div>

            {/* Delay between emails */}
            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1 flex items-center gap-1">
                <ShieldAlert className="w-3 h-3 text-slate-500" />
                Delay Between Emails
              </label>
              <div className="flex items-center gap-1">
                <input
                  type="number"
                  min={1}
                  max={300}
                  value={delayBetweenSeconds}
                  onChange={(e) => setDelayBetweenSeconds(Number(e.target.value))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                <span className="text-xs text-slate-400">sec</span>
              </div>
              <span className="text-[10px] text-slate-500">Throttling spacing</span>
            </div>

            {/* Hourly Limit */}
            <div>
              <label className="block text-[11px] font-medium text-slate-400 mb-1 flex items-center gap-1">
                <ShieldAlert className="w-3 h-3 text-slate-500" />
                Hourly Limit / Sender
              </label>
              <div className="flex items-center gap-1">
                <input
                  type="number"
                  min={1}
                  max={5000}
                  value={hourlyLimit}
                  onChange={(e) => setHourlyLimit(Number(e.target.value))}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                <span className="text-xs text-slate-400">/hr</span>
              </div>
              <span className="text-[10px] text-slate-500">Auto-reschedules surplus</span>
            </div>
          </div>

          {/* Modal Footer */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex items-center gap-2 px-5 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-lg transition shadow-lg shadow-blue-600/20"
            >
              {isSubmitting ? (
                <>
                  <span className="w-3.5 h-3.5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                  <span>Scheduling Jobs...</span>
                </>
              ) : (
                <>
                  <Mail className="w-3.5 h-3.5" />
                  <span>
                    Schedule {detectedEmails.length > 0 ? `${detectedEmails.length} Emails` : 'Campaign'}
                  </span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
