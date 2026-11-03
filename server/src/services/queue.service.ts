import { Queue } from 'bullmq';
import { redisConnection } from '../config/redis.js';
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

export const EMAIL_QUEUE_NAME = 'email-scheduler-queue';

export interface EmailJobPayload {
  id: string; // Database EmailJob id
  userId: string;
  recipientEmail: string;
  senderEmail: string;
  subject: string;
  body: string;
  scheduledAt: string; // ISO string
  delayBetweenMs: number;
  hourlyLimit: number;
}

export const emailQueue = new Queue<EmailJobPayload>(EMAIL_QUEUE_NAME, {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 5000,
    },
    removeOnComplete: {
      age: 24 * 3600, // Keep completed jobs for 24h in Bull-Board
      count: 1000,
    },
    removeOnFail: {
      age: 7 * 24 * 3600,
    },
  },
});

emailQueue.on('error', (err) => {
  console.error('[BullMQ Queue] Error:', err.message);
});

/**
 * Bull-Board live queue monitoring setup
 */
export const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

createBullBoard({
  queues: [new BullMQAdapter(emailQueue)],
  serverAdapter,
});

/**
 * Adds an email job to BullMQ queue with exact delay (No Cron!)
 */
export async function addEmailJobToQueue(jobData: EmailJobPayload, explicitDelayMs?: number) {
  const scheduledTime = new Date(jobData.scheduledAt).getTime();
  const now = Date.now();
  const delay = explicitDelayMs !== undefined ? explicitDelayMs : Math.max(0, scheduledTime - now);

  return emailQueue.add('send-email', jobData, {
    delay,
    jobId: jobData.id, // Idempotency key: prevents duplicate jobs
  });
}
