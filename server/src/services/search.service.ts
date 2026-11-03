import { getElasticsearchClient, isElasticsearchAvailable } from '../config/elasticsearch.js';
import { config } from '../config/env.js';
import { prisma } from '../config/prisma.js';
import { EmailStatus } from '@prisma/client';

export class SearchService {
  /**
   * Index or update an email in Elasticsearch
   */
  public static async indexEmail(emailJob: {
    id: string;
    userId: string;
    recipientEmail: string;
    senderEmail: string;
    subject: string;
    body: string;
    status: EmailStatus;
    scheduledAt: Date;
    sentAt?: Date | null;
    etherealUrl?: string | null;
    createdAt: Date;
  }): Promise<void> {
    if (!isElasticsearchAvailable()) return;

    try {
      const client = getElasticsearchClient();
      await client.index({
        index: config.elasticsearch.index,
        id: emailJob.id,
        document: {
          id: emailJob.id,
          userId: emailJob.userId,
          recipientEmail: emailJob.recipientEmail,
          senderEmail: emailJob.senderEmail,
          subject: emailJob.subject,
          body: emailJob.body,
          status: emailJob.status,
          scheduledAt: emailJob.scheduledAt.toISOString(),
          sentAt: emailJob.sentAt ? emailJob.sentAt.toISOString() : null,
          etherealUrl: emailJob.etherealUrl || null,
          createdAt: emailJob.createdAt.toISOString(),
        },
      });
    } catch (err: any) {
      console.warn(`[SearchService] Failed to index email in Elasticsearch (${err.message})`);
    }
  }

  /**
   * Search emails using Elasticsearch with fallback to Prisma ILIKE search
   */
  public static async searchEmails(params: {
    userId: string;
    query?: string;
    status?: EmailStatus | 'ALL';
    page?: number;
    pageSize?: number;
  }) {
    const { userId, query, status, page = 1, pageSize = 20 } = params;
    const skip = (page - 1) * pageSize;

    // Try Elasticsearch first if available and query is provided
    if (isElasticsearchAvailable() && query && query.trim() !== '') {
      try {
        const client = getElasticsearchClient();
        const mustClauses: any[] = [{ term: { userId } }];

        if (status && status !== 'ALL') {
          mustClauses.push({ term: { status } });
        }

        mustClauses.push({
          multi_match: {
            query: query.trim(),
            fields: ['recipientEmail^3', 'senderEmail^2', 'subject^2', 'body'],
            fuzziness: 'AUTO',
          },
        });

        const esResponse = await client.search({
          index: config.elasticsearch.index,
          from: skip,
          size: pageSize,
          query: {
            bool: {
              must: mustClauses,
            },
          },
          sort: [{ createdAt: { order: 'desc' } }],
        });

        const hits = esResponse.hits.hits;
        const total = typeof esResponse.hits.total === 'number' ? esResponse.hits.total : esResponse.hits.total?.value || 0;
        const results = hits.map((hit) => hit._source);

        return {
          source: 'elasticsearch',
          data: results,
          total,
          page,
          pageSize,
          totalPages: Math.ceil(total / pageSize),
        };
      } catch (err: any) {
        console.warn(`[SearchService] Elasticsearch query failed, falling back to PostgreSQL (${err.message})`);
      }
    }

    // Fallback to PostgreSQL Prisma query
    const whereClause: any = {
      userId,
    };

    if (status && status !== 'ALL') {
      whereClause.status = status;
    }

    if (query && query.trim() !== '') {
      const q = query.trim();
      whereClause.OR = [
        { recipientEmail: { contains: q, mode: 'insensitive' } },
        { senderEmail: { contains: q, mode: 'insensitive' } },
        { subject: { contains: q, mode: 'insensitive' } },
        { body: { contains: q, mode: 'insensitive' } },
      ];
    }

    const [total, data] = await Promise.all([
      prisma.emailJob.count({ where: whereClause }),
      prisma.emailJob.findMany({
        where: whereClause,
        orderBy: { scheduledAt: 'desc' },
        skip,
        take: pageSize,
      }),
    ]);

    return {
      source: 'postgresql',
      data,
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize),
    };
  }
}
