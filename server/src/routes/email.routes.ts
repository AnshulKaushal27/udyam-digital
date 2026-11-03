import { Router } from 'express';
import { EmailController } from '../controllers/email.controller.js';
import { requireAuth } from '../middleware/auth.middleware.js';

const router = Router();

router.use(requireAuth);

router.post('/schedule', EmailController.scheduleEmails);
router.get('/scheduled', EmailController.getScheduledEmails);
router.get('/sent', EmailController.getSentEmails);
router.get('/stats', EmailController.getEmailStats);

export default router;
