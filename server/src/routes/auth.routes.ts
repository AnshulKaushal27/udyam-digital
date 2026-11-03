import { Router } from 'express';
import { AuthController } from '../controllers/auth.controller.js';
import { requireAuth } from '../middleware/auth.middleware.js';

const router = Router();

router.post('/google', AuthController.googleLogin);
router.post('/demo', AuthController.demoLogin);
router.get('/profile', requireAuth, AuthController.getProfile);

export default router;
