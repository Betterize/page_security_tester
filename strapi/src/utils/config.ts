export class Config {
  REDIS_HOST: string;
  REDIS_PORT: number;
  REDIS_QUEUE_NAME: string;

  constructor() {
    this.REDIS_HOST = process.env.REDIS_HOST || "127.0.0.1";
    this.REDIS_PORT = Number(process.env.REDIS_PORT) || 6379;
    this.REDIS_QUEUE_NAME = process.env.REDIS_QUEUE_NAME || "security_tests";
  }
}
