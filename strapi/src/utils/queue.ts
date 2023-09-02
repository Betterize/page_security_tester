import * as redis from "redis";
import { Config } from "./config";
import { log, HookState } from "./logger";
import { notify_administrator } from "./email";

const config = new Config();

const redis_url = `redis://${config.REDIS_HOST}:${config.REDIS_PORT}`;

let is_error_reported = false;

const redisClient = redis
  .createClient({
    url: redis_url,
  })
  .on("error", (err) => {
    if (!is_error_reported) {
      is_error_reported = true;
      notify_administrator(`Redis client received error: ${err}`)
        .then(() => {
          log(
            "redis_queue",
            HookState.none,
            "Successfully send email notification"
          );
        })
        .catch((error) =>
          log(
            "redis_queue",
            HookState.none,
            `Unable to send email notification about error: ${err} Email error: ${error}`
          )
        );
    }
  });

let is_connected = false;

export async function notify_tests_runner(message: string) {
  if (!is_connected) {
    await redisClient.connect();
    is_connected = true;
  }
  await redisClient.lPush(config.REDIS_QUEUE_NAME, message);
}
