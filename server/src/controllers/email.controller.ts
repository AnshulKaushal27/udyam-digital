import { Response } from 'express';
import { z } from 'zod';
import { prisma } from '../config/prisma.js';
import { AuthRequest } from '../middleware/auth.middleware.js';
import { addEmailJobToQueue } from '../services/queue.service.js';
import { SearchService } from '../services/search.service.js';
import { EmailStatus } from '@prisma/client';
import { config } from '../config/env.js';

const scheduleSchema = z.object({
  recipients: z.array(z.string().email()).min(1, 'At least one recipient email is required'),
  senderEmail: z.string().email(),
  subject: z.string().min(1, 'Subject cannot be empty'),
  body: z.string().min(1, 'Body cannot be empty'),
  startTime: z.string().datetime().optional(),
  delayBetweenMs: z.number().min(500).default(config.worker.minDelayMs),
  hourlyLimit: z.number().min(1).default(config.worker.maxEmailsPerHour),
});

export class EmailController {
  /**
   * Schedule emails in batch from compose modal (CSV parsed leads)
   */
  public static async scheduleEmails(req: AuthRequest, res: Response): Promise<void> {
    try {
      const parsed = scheduleSchema.safeParse(req.body);
      if (!parsed.success) {
        res.status(400).json({ error: parsed.error.errors.map((e) => e.message).join(', ') });
        return;
      }

      const { recipients, senderEmail, subject, body, startTime, delayBetweenMs, hourlyLimit } = parsed.data;
      const userId = req.user!.id;

      const baseStartTime = startTime ? new Date(startTime).getTime() : Date.now();
      const createdJobs = [];

      for (let i = 0; i < recipients.length; i++) {
        const recipient = recipients[i].trim().toLowerCase();
        // Stagger email send times based on delayBetweenMs to avoid bursting
        const scheduledTime = new Date(baseStartTime + i * delayBetweenMs);

        // 1. Create in PostgreSQL
        const emailRecord = await prisma.emailJob.create({
          data: {
            userId,
            recipientEmail: recipient,
            senderEmail,
            subject,
            body,
            scheduledAt: scheduledTime,
            status: EmailStatus.SCHEDULED,
            delayBetweenMs,
            hourlyLimit,
          },
        });

        // 2. Add to BullMQ with computed delay
        const delay = Math.max(0, scheduledTime.getTime() - Date.now());
        const bullJob = await addEmailJobToQueue(
          {
            id: emailRecord.id,
            userId,
            recipientEmail: recipient,
            senderEmail,
            subject,
            body,
            scheduledAt: scheduledTime.toISOString(),
            delayBetweenMs,
            hourlyLimit,
          },
          delay
        );

        // Update bullMqJobId
        await prisma.emailJob.update({
          where: { id: emailRecord.id },
          data: { bullMqJobId: bullJob.id },
        });

        // 3. Index in Elasticsearch
        await SearchService.indexEmail({
          ...emailRecord,
          createdAt: emailRecord.createdAt,
        });

        createdJobs.push(emailRecord);
      }

      res.status(201).json({
        message: `Successfully scheduled ${createdJobs.length} email(s)`,
        count: createdJobs.length,
        jobs: createdJobs,
      });
    } catch (err: any) {
      console.error('[EmailController] Scheduling error:', err.message);
      res.status(500).json({ error: 'Failed to schedule emails: ' + err.message });
    }
  }

  /**
   * Get scheduled and delayed emails
   */
  public static async getScheduledEmails(req: AuthRequest, res: Response): Promise<void> {
    try {
      const userId = req.user!.id;
      const query = (req.query.q as string) || '';
      const page = Number(req.query.page) || 1;
      const pageSize = Number(req.query.pageSize) || 20;

      const results = await SearchService.searchEmails({
        userId,
        query,
        status: EmailStatus.SCHEDULED,
        page,
        pageSize,
      });

      res.json(results);
    } catch (err: any) {
      console.error('[EmailController] Error fetching scheduled emails:', err.message);
      res.status(500).json({ error: 'Failed to retrieve scheduled emails' });
    }
  }

  /**
   * Get sent and failed emails
   */
  public static async getSentEmails(req: AuthRequest, res: Response): Promise<void> {
    try {
      const userId = req.user!.id;
      const query = (req.query.q as string) || '';
      const page = Number(req.query.page) || 1;
      const pageSize = Number(req.query.pageSize) || 20;

      const results = await SearchService.searchEmails({
        userId,
        query,
        status: EmailStatus.SENT,
        page,
        pageSize,
      });

      res.json(results);
    } catch (err: any) {
      console.error('[EmailController] Error fetching sent emails:', err.message);
      res.status(500).json({ error: 'Failed to retrieve sent emails' });
    }
  }

  /**
   * Get overall email statistics for user dashboard
   */
  public static async getEmailStats(req: AuthRequest, res: Response): Promise<void> {
    try {
      const userId = req.user!.id;

      const [scheduledCount, delayedCount, sentCount, failedCount] = await Promise.all([
        prisma.emailJob.count({ where: { userId, status: EmailStatus.SCHEDULED } }),
        prisma.emailJob.count({ where: { userId, status: EmailStatus.DELAYED } }),
        prisma.emailJob.count({ where: { userId, status: EmailStatus.SENT } }),
        prisma.emailJob.count({ where: { userId, status: EmailStatus.FAILED } }),
      ]);

      res.json({
        scheduled: scheduledCount,
        delayed: delayedCount,
        sent: sentCount,
        failed: failedCount,
        total: scheduledCount + delayedCount + sentCount + failedCount,
      });
    } catch (err: any) {
      res.status(500).json({ error: 'Failed to fetch email statistics' });
    }
  }
}
