import { Redis } from 'ioredis';
import { config } from './env.js';

export const redisConnection = new Redis({
  host: config.redis.host,
  port: config.redis.port,
  password: config.redis.password,
  maxRetriesPerRequest: null,
  enableReadyCheck: false,
});

redisConnection.on('connect', () => {
  console.log('[Redis] Connected successfully to Redis server');
});

redisConnection.on('error', (err) => {
  console.error('[Redis] Connection error:', err.message);
});
