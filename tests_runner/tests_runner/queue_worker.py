from logging import log, INFO, ERROR
from config import Configuration
from strapi.send_strapi_info import update_scan_status
from schemas.security_scan import TestStatus, SecurityScanRequest
from exceptions.api import CustomFatalException
from typing import Callable
import time
import redis

from redis.exceptions import RedisError, ChildDeadlockedError, RedisClusterException


def serialize_message(message: bytes) -> SecurityScanRequest | None:
    try:
        decoded_message = message.decode('utf-8')
        log(INFO, f"received message: {decoded_message}")

        current_scan: SecurityScanRequest = SecurityScanRequest.from_json(decoded_message)
        log(INFO, "Successfully serialized data from queue")

        return current_scan

    except Exception as e:
        log(ERROR, f"Unable to serialize data. Message: {str(e)}")
        return None


def can_reconnect(failures: int) -> bool:
    await_time = {1: 30, 2: 60, 3: 90, 4: 120, 5: 180}

    if failures > max(list(await_time.keys())):
        log(ERROR, "To many attempts to fix redis connection")
        return False

    sleep_time = await_time[failures]

    log(INFO, f"Program will sleep for {sleep_time}s and then try to fix redis connection")
    time.sleep(sleep_time)

    return True


def read_from_queue(run_tests: Callable[[int, str], None]):
    config = Configuration()

    run: bool = True
    failure_counter: int = 0

    while run:
        try:
            redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
            log(INFO, "Successfully created redis client")

            failure_counter = 0

            while True:
                log(INFO, "--- ready to accept messages ---")

                _, message = redis_client.brpop(config.REDIS_QUEUE_NAME)

                current_scan = serialize_message(message=message)

                if current_scan is not None:
                    try:
                        run_tests(scan_id=current_scan.id, url=current_scan.website)

                    except CustomFatalException as e:
                        raise

                    except Exception as e:
                        log(ERROR, f"Exception ocurred while running scan. Message: {e}")
                        update_scan_status(id=current_scan.id, status=TestStatus.failed, error_ms=e)

        except RedisError as e:
            log(ERROR, f"Redis error occurred. Message: {e}")

            failure_counter = failure_counter + 1
            run = can_reconnect(failures=failure_counter)
