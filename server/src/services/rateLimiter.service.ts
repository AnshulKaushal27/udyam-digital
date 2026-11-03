import { redisConnection } from '../config/redis.js';
import { config } from '../config/env.js';

export interface RateLimitCheckResult {
  allowed: boolean;
  currentCount: number;
  hourlyLimit: number;
  delayUntilNextWindowMs: number;
  shouldNotifySlack: boolean;
}

export class RateLimiterService {
  /**
   * Generates the Redis key for a sender's current hourly window (UTC based).
   */
  private static getHourlyWindowKey(senderEmail: string, date: Date = new Date()): string {
    const year = date.getUTCFullYear();
    const month = String(date.getUTCMonth() + 1).padStart(2, '0');
    const day = String(date.getUTCDate()).padStart(2, '0');
    const hour = String(date.getUTCHours()).padStart(2, '0');
    return `ratelimit:hourly:${senderEmail}:${year}-${month}-${day}-${hour}`;
  }

  /**
   * Calculates milliseconds remaining until the beginning of the next hourly window.
   */
  public static getMillisecondsUntilNextHour(date: Date = new Date()): number {
    const nextHour = new Date(date);
    nextHour.setUTCHours(nextHour.getUTCHours() + 1, 0, 1, 0); // 1 second past next hour
    const diff = nextHour.getTime() - date.getTime();
    return Math.max(5000, diff);
  }

  /**
   * Checks and increments the hourly send counter for a given sender.
   * Atomic across multiple concurrent workers using Redis INCR.
   */
  public static async checkAndIncrementHourlyLimit(
    senderEmail: string,
    hourlyLimit: number = config.worker.maxEmailsPerHour
  ): Promise<RateLimitCheckResult> {
    const key = this.getHourlyWindowKey(senderEmail);
    const count = await redisConnection.incr(key);

    // If it's the first key access, set TTL for 2 hours (7200s) for automatic cleanup
    if (count === 1) {
      await redisConnection.expire(key, 7200);
    }

    const delayUntilNextWindowMs = this.getMillisecondsUntilNextHour();

    if (count > hourlyLimit) {
      // Check if we already alerted Slack for this sender in this hour
      const notifyKey = `ratelimit:notified:${key}`;
      const alreadyNotified = await redisConnection.set(notifyKey, '1', 'EX', 3600, 'NX');
      const shouldNotifySlack = alreadyNotified === 'OK';

      return {
        allowed: false,
        currentCount: count,
        hourlyLimit,
        delayUntilNextWindowMs,
        shouldNotifySlack,
      };
    }

    return {
      allowed: true,
      currentCount: count,
      hourlyLimit,
      delayUntilNextWindowMs: 0,
      shouldNotifySlack: false,
    };
  }

  /**
   * Enforces minimum spacing/delay between consecutive email sends from the same sender.
   */
  public static async enforceSenderSpacing(
    senderEmail: string,
    minDelayMs: number = config.worker.minDelayMs
  ): Promise<number> {
    const key = `sender:last_sent:${senderEmail}`;
    const now = Date.now();
    const lastSentStr = await redisConnection.get(key);

    if (lastSentStr) {
      const lastSent = Number(lastSentStr);
      const elapsed = now - lastSent;
      if (elapsed < minDelayMs) {
        return minDelayMs - elapsed;
      }
    }

    // Set current timestamp as last sent
    await redisConnection.set(key, now.toString(), 'PX', minDelayMs * 10);
    return 0;
  }
}
