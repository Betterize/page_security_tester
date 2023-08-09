import * as redis from "redis";
import { Config } from "./config";

const config = new Config();

const redis_url = `redis://${config.REDIS_HOST}:${config.REDIS_PORT}`;

const redisClient = redis.createClient({
  url: redis_url,
});

let is_connected = false;

export async function notify_tests_runner(message: string) {
  if (!is_connected) {
    await redisClient.connect();
    is_connected = true;
  }

  await redisClient.lPush(config.REDIS_QUEUE_NAME, message);
}
