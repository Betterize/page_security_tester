from wapiti import run_wapiti
from namp import run_namp
from utils.locations import test_results_dir
from utils.configs import Configuration
from schemas.security_scan import SecurityScanRequest
from schemas.security_scan import TestStatus
import time
import redis
from utils.send_strapi_info import update_scan_status, add_test_to_scan
from utils.log import setup_logger
from logging import log, INFO, ERROR

from schemas.security_scan import TestStatus, SecurityTest, TestTool

def run_test(scan_id: int, tool: TestTool, tests: list[SecurityTest], url: str, result_dir, fun):
    # powinno kopnąć błędem jak poniższy kod się nie skończy dobrze
    test_id, tests = add_test_to_scan(scan_id=scan_id, tool=tool, current_test_results=tests)
    
    try:
        result = fun(url=url, result_dir=result_dir)
        # update with tests results
    except Exception as e:
        # setup test as failed
        pass


def run_tests(scan_id: int, url: str):
    
    result_dir = test_results_dir(url)

    tests = []
    run_test(scan_id, TestTool.wapiti, tests, url, result_dir, run_wapiti)

    tests = []
    run_test(scan_id, TestTool.nmap, tests, url, result_dir, run_namp)


def read_from_queue(redis_client: 'typing.any', queue_name: str):
    while True:
        log(INFO, "--- ready to accept messages ---")

        _, message = redis_client.brpop(queue_name)
        decoded_message = message.decode('utf-8')
        log(INFO, f"received message: {decoded_message}")

        if decoded_message == "quit":
            log(INFO, "--- Exit triggered by quit message ---")
            return

        try:
            current_scan: SecurityScanRequest = SecurityScanRequest.from_json(decoded_message)
            log(INFO, "Successfully serialized data from queue")

            update_scan_status(id=current_scan.id, status=TestStatus.running)

            #run_tests(url=decoded_message)

        except Exception as e:
            log(ERROR, f"Error ocurred while running scan. Error: {e}")
            update_scan_status(id=current_scan.id, status=TestStatus.failed, error_ms=e)


def run_service():
    log(INFO, "application started")

    config = Configuration()
    log(INFO, f"Successfully loaded configuration")

    try:
        redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
        log(INFO, "Successfully created redis client")

        read_from_queue(redis_client=redis_client, queue_name=config.REDIS_QUEUE_NAME)

    except Exception as e:
        log(ERROR, f"Unable to create redis client: {e}")


if __name__ == "__main__":
    setup_logger()

    try:
        run_service()

    except Exception as e:
        log(ERROR, f"Fatal error occurred while application run. Error: {e}")
