import { Client } from '@elastic/elasticsearch';
import { config } from './env.js';

let esClient: Client | null = null;
let isConnected = false;

export function getElasticsearchClient(): Client {
  if (!esClient) {
    esClient = new Client({
      node: config.elasticsearch.node,
    });
  }
  return esClient;
}

export async function initElasticsearch(): Promise<boolean> {
  const client = getElasticsearchClient();
  try {
    const health = await client.cluster.health({});
    console.log(`[Elasticsearch] Connected! Cluster status: ${health.status}`);
    isConnected = true;

    // Check if index exists, create if not
    const exists = await client.indices.exists({ index: config.elasticsearch.index });
    if (!exists) {
      console.log(`[Elasticsearch] Creating index "${config.elasticsearch.index}"...`);
      await client.indices.create({
        index: config.elasticsearch.index,
        mappings: {
          properties: {
            id: { type: 'keyword' },
            userId: { type: 'keyword' },
            recipientEmail: { type: 'text', fields: { keyword: { type: 'keyword' } } },
            senderEmail: { type: 'text', fields: { keyword: { type: 'keyword' } } },
            subject: { type: 'text' },
            body: { type: 'text' },
            status: { type: 'keyword' },
            scheduledAt: { type: 'date' },
            sentAt: { type: 'date' },
            etherealUrl: { type: 'keyword' },
            createdAt: { type: 'date' },
          },
        },
      });
      console.log(`[Elasticsearch] Index "${config.elasticsearch.index}" created successfully.`);
    }
    return true;
  } catch (err: any) {
    console.warn(`[Elasticsearch] Notice: Elasticsearch not reachable at ${config.elasticsearch.node} (${err.message}). Falling back to relational DB search.`);
    isConnected = false;
    return false;
  }
}

export function isElasticsearchAvailable(): boolean {
  return isConnected;
}
