import { Request, Response } from 'express';
import { AuthRequest } from '../middleware/auth.middleware.js';
import { SlackService } from '../services/slack.service.js';
import { config } from '../config/env.js';

export class SlackController {
  /**
   * Generates and returns Slack OAuth authorization URL
   */
  public static async getAuthorizeUrl(req: AuthRequest, res: Response): Promise<void> {
    try {
      const userId = req.user!.id;
      const authorizeUrl = SlackService.getAuthorizeUrl(userId);
      res.json({ authorizeUrl });
    } catch (err: any) {
      res.status(500).json({ error: 'Failed to generate Slack authorization URL' });
    }
  }

  /**
   * OAuth callback redirect endpoint from Slack
   */
  public static async oauthCallback(req: Request, res: Response): Promise<void> {
    try {
      const code = req.query.code as string;
      const state = req.query.state as string;

      if (!code || !state) {
        res.redirect(`${config.frontendUrl}?slack_error=missing_code_or_state`);
        return;
      }

      await SlackService.handleOAuthCallback(code, state);
      res.redirect(`${config.frontendUrl}?slack_connected=true`);
    } catch (err: any) {
      console.error('[SlackController] OAuth error:', err.message);
      res.redirect(`${config.frontendUrl}?slack_error=${encodeURIComponent(err.message)}`);
    }
  }

  /**
   * Save Webhook URL directly (Zero-hassle integration for demo/evaluators)
   */
  public static async saveWebhook(req: AuthRequest, res: Response): Promise<void> {
    try {
      const { webhookUrl, channel } = req.body;
      if (!webhookUrl || !webhookUrl.startsWith('https://hooks.slack.com/')) {
        res.status(400).json({ error: 'Valid Slack incoming webhook URL is required (must start with https://hooks.slack.com/)' });
        return;
      }

      const slackConfig = await SlackService.saveWebhook(req.user!.id, webhookUrl, channel);
      res.json({ success: true, message: 'Slack webhook saved successfully', slackConfig });
    } catch (err: any) {
      res.status(500).json({ error: 'Failed to save Slack webhook: ' + err.message });
    }
  }

  /**
   * Disconnect Slack
   */
  public static async disconnect(req: AuthRequest, res: Response): Promise<void> {
    try {
      await SlackService.disconnectSlack(req.user!.id);
      res.json({ success: true, message: 'Slack disconnected successfully' });
    } catch (err: any) {
      res.status(500).json({ error: 'Failed to disconnect Slack' });
    }
  }

  /**
   * Send test notification to verify connection
   */
  public static async sendTestNotification(req: AuthRequest, res: Response): Promise<void> {
    try {
      const result = await SlackService.sendTestNotification(req.user!.id);
      if (result.success) {
        res.json(result);
      } else {
        res.status(400).json(result);
      }
    } catch (err: any) {
      res.status(500).json({ error: 'Failed to dispatch test notification: ' + err.message });
    }
  }
}
