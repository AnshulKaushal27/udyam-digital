import { Router } from 'express';
import { SlackController } from '../controllers/slack.controller.js';
import { requireAuth } from '../middleware/auth.middleware.js';

const router = Router();

// OAuth callback is public redirect from Slack
router.get('/callback', SlackController.oauthCallback);

// Protected routes
router.use(requireAuth);
router.get('/authorize-url', SlackController.getAuthorizeUrl);
router.post('/webhook', SlackController.saveWebhook);
router.post('/disconnect', SlackController.disconnect);
router.post('/test-notification', SlackController.sendTestNotification);

export default router;
