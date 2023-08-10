from wapiti import run_wapiti
from nmap import run_nmap, process_result
from utils.locations import test_results_dir
from utils.configs import Configuration
import time
import redis
from schemas.security_scan import TestStatus, SecurityTest, TestTool, NewSecurityTest, SecurityScanRequest
from utils.send_strapi_info import update_scan_status, add_test_to_scan, update_tests_results
from exceptions.api import UpdateTestResultsException
from utils.log import setup_logger
from logging import log, INFO, ERROR


def run_test(scan_id: int, tool: TestTool, tests: list[SecurityTest], url: str, result_dir, fun):
    log(INFO, f"Starting {tool.value} test")

    test_id, tests = add_test_to_scan(scan_id=scan_id, tool=tool, current_test_results=tests)

    try:
        start_time = time.time()
        command, result = fun(url=url, result_dir=result_dir)
        scan_time = "{:.2f}".format(time.time() - start_time)

        log(INFO, f"Finished {tool.value} test after {scan_time}s")

        if test_id is None:
            new_test = NewSecurityTest(tool=tool,
                                       scan_time=scan_time,
                                       command=command,
                                       result=result,
                                       status=TestStatus.finished)
            tests.append(new_test)
        else:
            for test in tests:
                if test["id"] == test_id:
                    test["scan_time"] = scan_time
                    test["command"] = command
                    test["result"] = result
                    test["status"] = TestStatus.finished.value

        tests = update_tests_results(scan_id=scan_id, test_results=tests)
        log(INFO, f"Added results of {tool.value} test to scan with id: {scan_id}")

        return tests

    except UpdateTestResultsException as e:
        log(ERROR, f"Test finish but results not send: {str(e)}")

    except Exception as e:
        log(ERROR, f"Error occurred while running test: {str(e)}")


def run_tests(scan_id: int, url: str):
    update_scan_status(scan_id, TestStatus.running)

    tests = [(TestTool.wapiti, run_wapiti), (TestTool.nmap, run_nmap)]
    result_dir: str = test_results_dir(url)

    results = []

    for tool, fun in tests:
        results = run_test(scan_id, tool, results, url, result_dir, fun)

    update_scan_status(scan_id, TestStatus.finished)


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

            run_tests(scan_id=current_scan.id, url=current_scan.website)

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
