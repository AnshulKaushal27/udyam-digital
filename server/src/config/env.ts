import dotenv from 'dotenv';
dotenv.config();

export const config = {
  port: Number(process.env.PORT) || 5000,
  nodeEnv: process.env.NODE_ENV || 'development',
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:5173',

  databaseUrl: process.env.DATABASE_URL || 'postgresql://postgres@localhost:5433/reachinbox_db?schema=public',

  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: Number(process.env.REDIS_PORT) || 6379,
    password: process.env.REDIS_PASSWORD || undefined,
  },

  worker: {
    concurrency: Number(process.env.WORKER_CONCURRENCY) || 5,
    minDelayMs: Number(process.env.MIN_EMAIL_DELAY_MS) || 2000,
    maxEmailsPerHour: Number(process.env.MAX_EMAILS_PER_HOUR) || 50,
  },

  jwtSecret: process.env.JWT_SECRET || 'reachinbox_default_secret_jwt_2026',

  google: {
    clientId: process.env.GOOGLE_CLIENT_ID || '',
    clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
  },

  slack: {
    clientId: process.env.SLACK_CLIENT_ID || '',
    clientSecret: process.env.SLACK_CLIENT_SECRET || '',
    redirectUri: process.env.SLACK_REDIRECT_URI || 'http://localhost:5000/api/slack/callback',
  },

  elasticsearch: {
    node: process.env.ELASTICSEARCH_NODE || 'http://localhost:9200',
    index: process.env.ELASTICSEARCH_INDEX || 'reachinbox_emails',
  },

  ethereal: {
    user: process.env.ETHEREAL_USER || '',
    pass: process.env.ETHEREAL_PASS || '',
  },
};
