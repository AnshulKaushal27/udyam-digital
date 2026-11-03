import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config/env.js';
import { prisma } from '../config/prisma.js';

export interface AuthenticatedUser {
  id: string;
  email: string;
  name: string;
  avatarUrl?: string | null;
}

export interface AuthRequest extends Request {
  user?: AuthenticatedUser;
}

export async function requireAuth(req: AuthRequest, res: Response, next: NextFunction): Promise<void> {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ error: 'Unauthorized: Missing or invalid token format' });
      return;
    }

    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, config.jwtSecret) as { userId: string };

    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
      select: { id: true, email: true, name: true, avatarUrl: true },
    });

    if (!user) {
      res.status(401).json({ error: 'Unauthorized: User does not exist' });
      return;
    }

    req.user = user;
    next();
  } catch (err: any) {
    res.status(401).json({ error: 'Unauthorized: Invalid or expired token' });
  }
}
