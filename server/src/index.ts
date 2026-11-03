import express from 'express';
import cors from 'cors';
import { config } from './config/env.js';
import { serverAdapter } from './services/queue.service.js';
import authRoutes from './routes/auth.routes.js';
import emailRoutes from './routes/email.routes.js';
import slackRoutes from './routes/slack.routes.js';
import { initElasticsearch } from './config/elasticsearch.js';
import { getMailerTransporter } from './config/mailer.js';
import { EmailWorkerService } from './services/worker.service.js';
import { ReconciliationService } from './services/reconciliation.service.js';

const app = express();

// Middlewares
app.use(
  cors({
    origin: '*',
    credentials: true,
  })
);
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Live BullMQ Queue Monitoring Dashboard
app.use('/admin/queues', serverAdapter.getRouter());

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/emails', emailRoutes);
app.use('/api/slack', slackRoutes);

// Health Check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'reachinbox-scheduler-server',
    version: '1.0.0',
    bullBoardUrl: `http://localhost:${config.port}/admin/queues`,
  });
});

// Start Server & Background Services
const server = app.listen(config.port, async () => {
  console.log('====================================================');
  console.log(`🚀 ReachInbox Email Scheduler API running on port ${config.port}`);
  console.log(`📊 Bull-Board Live Queue Dashboard: http://localhost:${config.port}/admin/queues`);
  console.log(`🔗 API Base URL: http://localhost:${config.port}/api`);
  console.log('====================================================');

  try {
    // 1. Initialize Ethereal Mailer Transporter
    await getMailerTransporter();

    // 2. Initialize Elasticsearch (with graceful fallback)
    await initElasticsearch();

    // 3. Reconcile pending jobs on boot (Persistence & Zero loss on restart)
    await ReconciliationService.reconcilePendingJobs();

    // 4. Start BullMQ background worker
    EmailWorkerService.startWorker();
  } catch (initErr: any) {
    console.error('Error during startup initialization:', initErr.message);
  }
});

// Graceful Shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM signal received: closing HTTP server and BullMQ worker');
  await EmailWorkerService.closeWorker();
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});

process.on('SIGINT', async () => {
  console.log('SIGINT signal received: closing HTTP server and BullMQ worker');
  await EmailWorkerService.closeWorker();
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});

export default app;
