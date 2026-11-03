import axios from 'axios';
import type { EmailJob, EmailStats, User } from '../types';

const api = axios.create({
  baseURL: '/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('reachinbox_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  loginWithGoogle: async (credential: string) => {
    const res = await api.post<{ token: string; user: User }>('/auth/google', { credential });
    return res.data;
  },
  demoLogin: async () => {
    const res = await api.post<{ token: string; user: User }>('/auth/demo');
    return res.data;
  },
  getProfile: async () => {
    const res = await api.get<{ user: User }>('/auth/profile');
    return res.data.user;
  },
};

export const emailApi = {
  scheduleEmails: async (data: {
    recipients: string[];
    senderEmail: string;
    subject: string;
    body: string;
    startTime?: string;
    delayBetweenMs: number;
    hourlyLimit: number;
  }) => {
    const res = await api.post<{ message: string; count: number; jobs: EmailJob[] }>('/emails/schedule', data);
    return res.data;
  },
  getScheduledEmails: async (query?: string, page = 1, pageSize = 20) => {
    const res = await api.get<{
      source: string;
      data: EmailJob[];
      total: number;
      page: number;
      pageSize: number;
      totalPages: number;
    }>('/emails/scheduled', {
      params: { q: query, page, pageSize },
    });
    return res.data;
  },
  getSentEmails: async (query?: string, page = 1, pageSize = 20) => {
    const res = await api.get<{
      source: string;
      data: EmailJob[];
      total: number;
      page: number;
      pageSize: number;
      totalPages: number;
    }>('/emails/sent', {
      params: { q: query, page, pageSize },
    });
    return res.data;
  },
  getEmailStats: async () => {
    const res = await api.get<EmailStats>('/emails/stats');
    return res.data;
  },
};

export const slackApi = {
  getAuthorizeUrl: async () => {
    const res = await api.get<{ authorizeUrl: string }>('/slack/authorize-url');
    return res.data.authorizeUrl;
  },
  saveWebhook: async (webhookUrl: string, channel?: string) => {
    const res = await api.post<{ success: boolean; message: string; slackConfig: any }>('/slack/webhook', {
      webhookUrl,
      channel,
    });
    return res.data;
  },
  disconnect: async () => {
    const res = await api.post<{ success: boolean; message: string }>('/slack/disconnect');
    return res.data;
  },
  sendTestNotification: async () => {
    const res = await api.post<{ success: boolean; message: string }>('/slack/test-notification');
    return res.data;
  },
};
