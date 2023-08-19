from logging import log, INFO, ERROR
from config import Configuration
from strapi.send_strapi_info import update_scan_status
from schemas.security_scan import TestStatus, SecurityScanRequest

import redis


def read_from_queue(run_tests):
    config = Configuration()

    redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    log(INFO, "Successfully created redis client")

    while True:
        log(INFO, "--- ready to accept messages ---")

        _, message = redis_client.brpop(config.REDIS_QUEUE_NAME)
        decoded_message = message.decode('utf-8')
        log(INFO, f"received message: {decoded_message}")

        if decoded_message == "quit":
            log(INFO, "--- Exit triggered by quit message ---")
            return

        try:
            current_scan: SecurityScanRequest = SecurityScanRequest.from_json(decoded_message)
            log(INFO, "Successfully serialized data from queue")

            run_tests(scan_id=current_scan.id, url=current_scan.website)

        except Exception as e:
            log(ERROR, f"Error ocurred while running scan. Error: {e}")
            update_scan_status(id=current_scan.id, status=TestStatus.failed, error_ms=e)
