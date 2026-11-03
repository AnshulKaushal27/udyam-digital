import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useAuth } from '../context/AuthContext';
import { Mail, Zap, Shield, Sparkles, ArrowRight, Server } from 'lucide-react';

export const LoginView: React.FC = () => {
  const { loginWithGoogle, loginDemo, isLoading } = useAuth();

  return (
    <div className="min-h-screen bg-[#0b0f19] flex flex-col justify-center items-center p-4 relative overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-blue-600/15 rounded-full blur-[130px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[250px] bg-indigo-600/10 rounded-full blur-[100px] pointer-events-none" />

      <div className="w-full max-w-md relative z-10">
        {/* Logo & Headline */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 shadow-xl shadow-blue-500/25 mb-4">
            <Mail className="w-7 h-7 text-white" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            ReachInbox Scheduler
          </h1>
          <p className="text-sm text-slate-400 mt-2 max-w-sm mx-auto">
            Production-Grade Full-Stack Email Job Scheduler with BullMQ, Redis, and Rate Limiting
          </p>
        </div>

        {/* Card */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl backdrop-blur-xl">
          <div className="space-y-4">
            {/* Feature Badges */}
            <div className="grid grid-cols-2 gap-2 pb-2">
              <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/40 border border-slate-700/40 text-[11px] text-slate-300">
                <Server className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                <span>Zero-Cron BullMQ</span>
              </div>
              <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/40 border border-slate-700/40 text-[11px] text-slate-300">
                <Shield className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Hourly Rate Limiter</span>
              </div>
              <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/40 border border-slate-700/40 text-[11px] text-slate-300">
                <Zap className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                <span>Slack Alerts</span>
              </div>
              <div className="flex items-center gap-2 p-2 rounded-lg bg-slate-800/40 border border-slate-700/40 text-[11px] text-slate-300">
                <Sparkles className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                <span>Elasticsearch Index</span>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800">
              <p className="text-xs font-semibold text-slate-300 text-center mb-3">
                Sign in to manage schedules & queues
              </p>

              {/* Real Google OAuth Login */}
              <div className="flex justify-center my-3">
                <GoogleLogin
                  onSuccess={(credentialResponse) => {
                    if (credentialResponse.credential) {
                      loginWithGoogle(credentialResponse.credential);
                    }
                  }}
                  onError={() => {
                    console.error('Google Login Error');
                  }}
                  theme="filled_black"
                  shape="pill"
                  size="large"
                  text="signin_with"
                />
              </div>

              <div className="relative flex py-2 items-center">
                <div className="flex-grow border-t border-slate-800"></div>
                <span className="flex-shrink mx-3 text-[10px] text-slate-500 uppercase tracking-widest">
                  Evaluator Fast-Track
                </span>
                <div className="flex-grow border-t border-slate-800"></div>
              </div>

              {/* Demo Login Button */}
              <button
                type="button"
                onClick={loginDemo}
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-blue-500/20 transition"
              >
                <span>Instant Demo Login (Candidate Account)</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-slate-500 mt-6">
          ReachInbox Hiring Assignment &bull; Built with Express, BullMQ, Redis & React
        </p>
      </div>
    </div>
  );
};
