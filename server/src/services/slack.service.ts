import axios from 'axios';
import { prisma } from '../config/prisma.js';
import { config } from '../config/env.js';

export class SlackService {
  /**
   * Generates the Slack OAuth 2.0 Authorization URL
   */
  public static getAuthorizeUrl(userId: string): string {
    const scopes = ['incoming-webhook', 'chat:write'];
    const state = Buffer.from(JSON.stringify({ userId, timestamp: Date.now() })).toString('base64');
    
    return `https://slack.com/oauth/v2/authorize?client_id=${config.slack.clientId}&scope=${scopes.join(',')}&redirect_uri=${encodeURIComponent(config.slack.redirectUri)}&state=${state}`;
  }

  /**
   * Exchanging Slack OAuth code for access token & webhook
   */
  public static async handleOAuthCallback(code: string, state: string) {
    try {
      const decodedState = JSON.parse(Buffer.from(state, 'base64').toString('utf-8'));
      const userId = decodedState.userId;

      const tokenResponse = await axios.post(
        'https://slack.com/api/oauth.v2.access',
        new URLSearchParams({
          client_id: config.slack.clientId,
          client_secret: config.slack.clientSecret,
          code,
          redirect_uri: config.slack.redirectUri,
        }).toString(),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      const data = tokenResponse.data;
      if (!data.ok) {
        throw new Error(`Slack OAuth error: ${data.error || 'Failed to exchange token'}`);
      }

      const webhookUrl = data.incoming_webhook?.url;
      const channel = data.incoming_webhook?.channel || data.incoming_webhook?.channel_id;
      const teamName = data.team?.name;
      const accessToken = data.access_token;

      // Upsert SlackConfig
      const slackConfig = await prisma.slackConfig.upsert({
        where: { userId },
        update: {
          accessToken,
          webhookUrl,
          channel,
          teamName,
          isConnected: true,
        },
        create: {
          userId,
          accessToken,
          webhookUrl,
          channel,
          teamName,
          isConnected: true,
        },
      });

      return { success: true, slackConfig };
    } catch (err: any) {
      console.error('[SlackService] OAuth callback failure:', err.message);
      throw err;
    }
  }

  /**
   * Saves or updates a direct Slack Webhook URL (ideal for instant zero-hassle testing)
   */
  public static async saveWebhook(userId: string, webhookUrl: string, channelName?: string) {
    return prisma.slackConfig.upsert({
      where: { userId },
      update: {
        webhookUrl,
        channel: channelName || '#general',
        isConnected: true,
      },
      create: {
        userId,
        webhookUrl,
        channel: channelName || '#general',
        isConnected: true,
      },
    });
  }

  /**
   * Disconnects Slack integration
   */
  public static async disconnectSlack(userId: string) {
    return prisma.slackConfig.updateMany({
      where: { userId },
      data: {
        isConnected: false,
        accessToken: null,
        webhookUrl: null,
      },
    });
  }

  /**
   * Dispatches live Rate Limit Alert message to user's Slack
   */
  public static async notifyRateLimitHit(
    userId: string,
    senderEmail: string,
    currentCount: number,
    hourlyLimit: number,
    rescheduledDelayMs: number
  ): Promise<boolean> {
    try {
      const slackConfig = await prisma.slackConfig.findUnique({
        where: { userId },
      });

      if (!slackConfig || !slackConfig.isConnected) {
        console.log(`[SlackService] User ${userId} has not connected Slack. Skipping rate-limit notification.`);
        return false;
      }

      const minutesUntilNextWindow = Math.round(rescheduledDelayMs / 60000);
      const payload = {
        text: `⚠️ *ReachInbox Rate Limit Alert*: Sender \`${senderEmail}\` reached hourly capacity!`,
        blocks: [
          {
            type: 'header',
            text: {
              type: 'plain_text',
              text: '🚨 ReachInbox Email Scheduler: Rate Limit Hit',
              emoji: true,
            },
          },
          {
            type: 'section',
            fields: [
              {
                type: 'mrkdwn',
                text: `*Sender:*\n\`${senderEmail}\``,
              },
              {
                type: 'mrkdwn',
                text: `*Hourly Limit:*\n${hourlyLimit} emails/hr`,
              },
              {
                type: 'mrkdwn',
                text: `*Current Attempt:*\n${currentCount} attempts`,
              },
              {
                type: 'mrkdwn',
                text: `*Auto-Reschedule Delay:*\n~${minutesUntilNextWindow} minutes`,
              },
            ],
          },
          {
            type: 'context',
            elements: [
              {
                type: 'mrkdwn',
                text: `ℹ️ *No emails were dropped.* All surplus jobs have been automatically queued for the next hour window.`,
              },
            ],
          },
        ],
      };

      if (slackConfig.webhookUrl) {
        await axios.post(slackConfig.webhookUrl, payload, { timeout: 10000 });
        console.log(`[SlackService] Sent rate-limit notification to Slack via Webhook for sender ${senderEmail}`);
        return true;
      }

      if (slackConfig.accessToken && slackConfig.channel) {
        await axios.post(
          'https://slack.com/api/chat.postMessage',
          {
            channel: slackConfig.channel,
            ...payload,
          },
          {
            headers: {
              Authorization: `Bearer ${slackConfig.accessToken}`,
              'Content-Type': 'application/json',
            },
            timeout: 10000,
          }
        );
        console.log(`[SlackService] Sent rate-limit notification to Slack via Bot Token for sender ${senderEmail}`);
        return true;
      }

      return false;
    } catch (err: any) {
      console.error(`[SlackService] Failed to send Slack alert:`, err.response?.data || err.message);
      return false;
    }
  }

  /**
   * Sends a test verification notification to verify connectivity from dashboard
   */
  public static async sendTestNotification(userId: string): Promise<{ success: boolean; message: string }> {
    const slackConfig = await prisma.slackConfig.findUnique({
      where: { userId },
    });

    if (!slackConfig || !slackConfig.isConnected || !slackConfig.webhookUrl) {
      return { success: false, message: 'Slack is not connected. Please connect Slack first.' };
    }

    try {
      await axios.post(
        slackConfig.webhookUrl,
        {
          text: '✅ *ReachInbox Test Notification*: Slack is successfully connected and receiving events!',
          blocks: [
            {
              type: 'section',
              text: {
                type: 'mrkdwn',
                text: '🎉 *ReachInbox Integration Verified!* Your Slack notifications are active and ready for live rate-limit events.',
              },
            },
          ],
        },
        { timeout: 8000 }
      );
      return { success: true, message: 'Test message sent to Slack successfully!' };
    } catch (err: any) {
      return { success: false, message: err.response?.data?.message || err.message };
    }
  }
}
