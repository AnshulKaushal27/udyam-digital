import { Worker, Job } from 'bullmq';
import { redisConnection } from '../config/redis.js';
import { EMAIL_QUEUE_NAME, EmailJobPayload, emailQueue } from './queue.service.js';
import { config } from '../config/env.js';
import { prisma } from '../config/prisma.js';
import { getMailerTransporter, getEtherealPreviewUrl } from '../config/mailer.js';
import { RateLimiterService } from './rateLimiter.service.js';
import { SlackService } from './slack.service.js';
import { SearchService } from './search.service.js';
import { EmailStatus } from '@prisma/client';

export class EmailWorkerService {
  private static workerInstance: Worker<EmailJobPayload> | null = null;

  public static startWorker() {
    if (this.workerInstance) {
      return this.workerInstance;
    }

    const concurrency = config.worker.concurrency;
    console.log(`[BullMQ Worker] Initializing email worker with concurrency: ${concurrency}`);

    this.workerInstance = new Worker<EmailJobPayload>(
      EMAIL_QUEUE_NAME,
      async (job: Job<EmailJobPayload>) => {
        return this.processJob(job);
      },
      {
        connection: redisConnection,
        concurrency,
      }
    );

    this.workerInstance.on('completed', (job) => {
      console.log(`[BullMQ Worker] Job ${job.id} completed successfully for recipient: ${job.data.recipientEmail}`);
    });

    this.workerInstance.on('failed', (job, err) => {
      console.error(`[BullMQ Worker] Job ${job?.id} failed with error: ${err.message}`);
    });

    this.workerInstance.on('error', (err) => {
      console.error('[BullMQ Worker] Unhandled worker error:', err.message);
    });

    return this.workerInstance;
  }

  private static async processJob(job: Job<EmailJobPayload>) {
    const { id, userId, recipientEmail, senderEmail, subject, body, delayBetweenMs, hourlyLimit } = job.data;
    console.log(`[BullMQ Worker] Processing job ${id} (Sender: ${senderEmail} -> Recipient: ${recipientEmail})`);

    // 1. Verify job in DB
    const emailRecord = await prisma.emailJob.findUnique({ where: { id } });
    if (!emailRecord) {
      console.warn(`[BullMQ Worker] Job record ${id} not found in database. Skipping.`);
      return;
    }

    // 2. Check Hourly Rate Limit across all workers/instances
    const rateLimitResult = await RateLimiterService.checkAndIncrementHourlyLimit(senderEmail, hourlyLimit);

    if (!rateLimitResult.allowed) {
      console.warn(
        `[BullMQ Worker] Hourly limit (${hourlyLimit}) reached for sender ${senderEmail}. (Attempt: ${rateLimitResult.currentCount}). Rescheduling job into next hour window (~${Math.round(rateLimitResult.delayUntilNextWindowMs / 60000)} mins).`
      );

      // Reschedule job into next hour window (Never drop or fail jobs!)
      const nextWindowTime = new Date(Date.now() + rateLimitResult.delayUntilNextWindowMs);
      await prisma.emailJob.update({
        where: { id },
        data: {
          status: EmailStatus.DELAYED,
          scheduledAt: nextWindowTime,
        },
      });

      // Notify Slack if not yet notified for this hour window
      if (rateLimitResult.shouldNotifySlack) {
        await SlackService.notifyRateLimitHit(
          userId,
          senderEmail,
          rateLimitResult.currentCount,
          hourlyLimit,
          rateLimitResult.delayUntilNextWindowMs
        );
      }

      // Re-add to queue with delay
      await emailQueue.add(
        'send-email',
        {
          ...job.data,
          scheduledAt: nextWindowTime.toISOString(),
        },
        {
          delay: rateLimitResult.delayUntilNextWindowMs,
          jobId: `${id}-rescheduled-${Date.now()}`,
        }
      );

      return { status: 'RESCHEDULED', delayUntilNextWindowMs: rateLimitResult.delayUntilNextWindowMs };
    }

    // 3. Check and enforce inter-email minimum delay per sender (Throttling guard)
    const requiredSpacingMs = await RateLimiterService.enforceSenderSpacing(senderEmail, delayBetweenMs || config.worker.minDelayMs);
    if (requiredSpacingMs > 0) {
      console.log(`[BullMQ Worker] Throttling sender ${senderEmail}. Waiting ${requiredSpacingMs}ms to maintain inter-email delay.`);
      await new Promise((resolve) => setTimeout(resolve, requiredSpacingMs));
    }

    // 4. Send Email via Ethereal SMTP
    try {
      const transporter = await getMailerTransporter();
      const info = await transporter.sendMail({
        from: `"${senderEmail}" <${senderEmail}>`,
        to: recipientEmail,
        subject,
        text: body,
        html: `<div style="font-family: sans-serif; padding: 16px;">${body.replace(/\n/g, '<br/>')}</div>`,
      });

      const previewUrl = getEtherealPreviewUrl(info) || `https://ethereal.email/message/${info.messageId}`;
      const sentTime = new Date();

      // Update Database status
      const updated = await prisma.emailJob.update({
        where: { id },
        data: {
          status: EmailStatus.SENT,
          sentAt: sentTime,
          etherealUrl: previewUrl,
        },
      });

      // Update Elasticsearch Index
      await SearchService.indexEmail({
        ...updated,
        createdAt: updated.createdAt,
      });

      console.log(`[BullMQ Worker] Successfully sent email to ${recipientEmail}. Preview: ${previewUrl}`);
      return { status: 'SENT', messageId: info.messageId, previewUrl };
    } catch (sendErr: any) {
      console.error(`[BullMQ Worker] Failed to send email to ${recipientEmail}:`, sendErr.message);

      await prisma.emailJob.update({
        where: { id },
        data: {
          status: EmailStatus.FAILED,
          errorMessage: sendErr.message,
        },
      });

      throw sendErr;
    }
  }

  public static async closeWorker() {
    if (this.workerInstance) {
      await this.workerInstance.close();
      this.workerInstance = null;
    }
  }
}
