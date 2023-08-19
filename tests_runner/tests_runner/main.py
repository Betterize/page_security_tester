from utils.locations import results_dir
from strapi.wapiti_classifications import add_classifications
from schemas.security_scan import TestStatus, SecurityTest, NewSecurityTest
from strapi.send_strapi_info import update_scan_status, add_test_to_scan, update_tests_results
from exceptions.api import UpdateTestResultsException
from utils.log import setup_logger
from logging import log, INFO, ERROR
from queue_worker import read_from_queue
from scan_tools.nmap import NmapScan
from scan_tools.wapiti import WapitiScan
from scan_tools.scan_tool import ScanTool


def run_test(scan_id: int, tests_results: list[SecurityTest], scan_tool: ScanTool):
    tool = scan_tool.tool_name()

    log(INFO, f"Starting {tool.value} test")

    test_id, tests_results = add_test_to_scan(scan_id=scan_id, tool=tool, current_test_results=tests_results)

    try:
        command, result, scan_time = scan_tool.run_scan()

        if test_id is None:
            new_test = NewSecurityTest(tool=tool,
                                       scan_time=scan_time,
                                       command=command,
                                       result=result,
                                       status=TestStatus.finished)
            tests_results.append(new_test)
        else:
            for test in tests_results:
                if test["id"] == test_id:
                    test["scan_time"] = scan_time
                    test["command"] = command
                    test["result"] = result
                    test["status"] = TestStatus.finished.value

        tests_results = update_tests_results(scan_id=scan_id, test_results=tests_results)
        log(INFO, f"Added results of {tool.value} test to scan with id: {scan_id}")

        return tests_results

    except UpdateTestResultsException as e:
        log(ERROR, f"Test finish but results not send: {str(e)}")

    except Exception as e:
        log(ERROR, f"Error occurred while running test: {str(e)}")


def run_tests(scan_id: int, url: str):
    update_scan_status(scan_id, TestStatus.running)

    result_dir: str = results_dir(url)

    tests: list[ScanTool] = [
        WapitiScan(result_directory=result_dir, url=url),
        NmapScan(result_directory=result_dir, url=url)
    ]

    results = []

    for scan_tool in tests:
        results = run_test(scan_id=scan_id, tests_results=results, scan_tool=scan_tool)

    update_scan_status(scan_id, TestStatus.finished)


def run_service():
    try:
        read_from_queue(run_tests=run_tests)

    except Exception as e:
        log(ERROR, f"Unable to create redis client: {e}")


if __name__ == "__main__":
    setup_logger()
    add_classifications()

    try:
        log(INFO, "application started")
        run_service()

    except Exception as e:
        log(ERROR, f"Fatal error occurred while application run. Error: {e}")
