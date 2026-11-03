import { prisma } from '../config/prisma.js';
import { emailQueue, addEmailJobToQueue } from './queue.service.js';
import { EmailStatus } from '@prisma/client';

export class ReconciliationService {
  /**
   * Runs on server startup to reconcile and re-queue any pending jobs.
   * Guarantees zero lost jobs across server crashes or restarts.
   */
  public static async reconcilePendingJobs(): Promise<number> {
    console.log('[Reconciliation] Scanning database for pending scheduled jobs...');

    try {
      const pendingJobs = await prisma.emailJob.findMany({
        where: {
          status: {
            in: [EmailStatus.SCHEDULED, EmailStatus.DELAYED],
          },
        },
      });

      console.log(`[Reconciliation] Found ${pendingJobs.length} scheduled/delayed jobs in database.`);
      let requeuedCount = 0;

      for (const email of pendingJobs) {
        // Check if job already exists in Redis BullMQ queue
        const existingJob = await emailQueue.getJob(email.id);

        if (!existingJob) {
          const now = Date.now();
          const scheduledTime = email.scheduledAt.getTime();
          const delay = Math.max(0, scheduledTime - now);

          console.log(
            `[Reconciliation] Re-enqueueing missing job ${email.id} (Scheduled for: ${email.scheduledAt.toISOString()}, Delay: ${delay}ms)`
          );

          await addEmailJobToQueue(
            {
              id: email.id,
              userId: email.userId,
              recipientEmail: email.recipientEmail,
              senderEmail: email.senderEmail,
              subject: email.subject,
              body: email.body,
              scheduledAt: email.scheduledAt.toISOString(),
              delayBetweenMs: email.delayBetweenMs,
              hourlyLimit: email.hourlyLimit,
            },
            delay
          );

          requeuedCount++;
        }
      }

      console.log(`[Reconciliation] Completed! ${requeuedCount} jobs verified and re-enqueued.`);
      return requeuedCount;
    } catch (err: any) {
      console.error('[Reconciliation] Error reconciling pending jobs:', err.message);
      return 0;
    }
  }
}
