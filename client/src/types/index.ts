export type EmailStatus = 'SCHEDULED' | 'DELAYED' | 'SENT' | 'FAILED';

export interface User {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string | null;
  slackConfig?: SlackConfig | null;
}

export interface SlackConfig {
  id: string;
  isConnected: boolean;
  channel?: string | null;
  teamName?: string | null;
  webhookUrl?: string | null;
}

export interface EmailJob {
  id: string;
  userId: string;
  recipientEmail: string;
  senderEmail: string;
  subject: string;
  body: string;
  scheduledAt: string;
  sentAt?: string | null;
  status: EmailStatus;
  bullMqJobId?: string | null;
  etherealUrl?: string | null;
  errorMessage?: string | null;
  delayBetweenMs: number;
  hourlyLimit: number;
  createdAt: string;
  updatedAt: string;
}

export interface EmailStats {
  scheduled: number;
  delayed: number;
  sent: number;
  failed: number;
  total: number;
}
