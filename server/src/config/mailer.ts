import nodemailer from 'nodemailer';
import { config } from './env.js';

let transporterInstance: nodemailer.Transporter | null = null;

export async function getMailerTransporter(): Promise<nodemailer.Transporter> {
  if (transporterInstance) {
    return transporterInstance;
  }

  let user = config.ethereal.user;
  let pass = config.ethereal.pass;

  if (!user || !pass) {
    console.log('[Mailer] No Ethereal credentials supplied. Generating test account on Ethereal Email...');
    const testAccount = await nodemailer.createTestAccount();
    user = testAccount.user;
    pass = testAccount.pass;
    console.log(`[Mailer] Test account generated!`);
    console.log(`[Mailer] Ethereal User: ${user}`);
    console.log(`[Mailer] Ethereal Web Login: https://ethereal.email/login`);
  }

  transporterInstance = nodemailer.createTransport({
    host: 'smtp.ethereal.email',
    port: 587,
    secure: false, // true for 465, false for other ports
    auth: {
      user,
      pass,
    },
  });

  return transporterInstance;
}

export function getEtherealPreviewUrl(info: nodemailer.SentMessageInfo): string | false {
  return nodemailer.getTestMessageUrl(info);
}
