import { Request, Response } from 'express';
import { OAuth2Client } from 'google-auth-library';
import jwt from 'jsonwebtoken';
import { prisma } from '../config/prisma.js';
import { config } from '../config/env.js';
import { AuthRequest } from '../middleware/auth.middleware.js';

const googleClient = new OAuth2Client(config.google.clientId);

export class AuthController {
  /**
   * Real Google OAuth Login: Verifies Google ID token from frontend
   */
  public static async googleLogin(req: Request, res: Response): Promise<void> {
    try {
      const { credential } = req.body;

      if (!credential) {
        res.status(400).json({ error: 'Google credential token is required' });
        return;
      }

      let payload: any;

      if (config.google.clientId) {
        const ticket = await googleClient.verifyIdToken({
          idToken: credential,
          audience: config.google.clientId,
        });
        payload = ticket.getPayload();
      } else {
        // Fallback for decoding unverified JWT if client ID not configured
        const decoded = jwt.decode(credential) as any;
        if (!decoded || !decoded.email) {
          res.status(400).json({ error: 'Invalid Google credential token' });
          return;
        }
        payload = decoded;
      }

      if (!payload || !payload.email) {
        res.status(400).json({ error: 'Invalid Google token payload' });
        return;
      }

      const googleId = payload.sub || `google-${Date.now()}`;
      const email = payload.email.toLowerCase();
      const name = payload.name || email.split('@')[0];
      const avatarUrl = payload.picture || null;

      // Upsert user in PostgreSQL
      const user = await prisma.user.upsert({
        where: { email },
        update: {
          name,
          avatarUrl,
          googleId,
        },
        create: {
          email,
          name,
          avatarUrl,
          googleId,
        },
        select: {
          id: true,
          email: true,
          name: true,
          avatarUrl: true,
          slackConfig: {
            select: {
              isConnected: true,
              channel: true,
              teamName: true,
            },
          },
        },
      });

      // Sign JWT session token
      const token = jwt.sign({ userId: user.id }, config.jwtSecret, { expiresIn: '7d' });

      res.json({
        token,
        user,
      });
    } catch (err: any) {
      console.error('[AuthController] Google login error:', err.message);
      res.status(500).json({ error: 'Google authentication failed: ' + err.message });
    }
  }

  /**
   * Demo / Fast-Track Login for instant evaluation without requiring Google Cloud credentials
   */
  public static async demoLogin(req: Request, res: Response): Promise<void> {
    try {
      const demoEmail = 'reachinbox.candidate@outboxlabs.com';
      const demoName = 'ReachInbox Candidate';
      const demoAvatar = 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80';

      const user = await prisma.user.upsert({
        where: { email: demoEmail },
        update: {
          name: demoName,
          avatarUrl: demoAvatar,
        },
        create: {
          email: demoEmail,
          name: demoName,
          avatarUrl: demoAvatar,
          googleId: 'demo-google-id-001',
        },
        select: {
          id: true,
          email: true,
          name: true,
          avatarUrl: true,
          slackConfig: {
            select: {
              isConnected: true,
              channel: true,
              teamName: true,
            },
          },
        },
      });

      const token = jwt.sign({ userId: user.id }, config.jwtSecret, { expiresIn: '7d' });

      res.json({
        token,
        user,
      });
    } catch (err: any) {
      console.error('[AuthController] Demo login error:', err.message);
      res.status(500).json({ error: 'Demo authentication failed: ' + err.message });
    }
  }

  /**
   * Get current authenticated user profile
   */
  public static async getProfile(req: AuthRequest, res: Response): Promise<void> {
    try {
      const user = await prisma.user.findUnique({
        where: { id: req.user!.id },
        select: {
          id: true,
          email: true,
          name: true,
          avatarUrl: true,
          slackConfig: {
            select: {
              isConnected: true,
              channel: true,
              teamName: true,
              webhookUrl: true,
            },
          },
        },
      });

      if (!user) {
        res.status(404).json({ error: 'User not found' });
        return;
      }

      res.json({ user });
    } catch (err: any) {
      res.status(500).json({ error: 'Failed to fetch user profile' });
    }
  }
}
