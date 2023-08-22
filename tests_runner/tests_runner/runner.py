from queue_worker import read_from_queue
from exceptions.api import CustomFatalException
from exceptions.scan_tools import ScanTestFailed
from scan_tools.nmap import NmapScan
from scan_tools.wapiti import WapitiScan
from scan_tools.scan_tool import ScanTool
from schemas.security_scan import TestStatus, SecurityTest, NewSecurityTest, RunScanResult, TestTool
from strapi.send_strapi_info import update_scan_status, add_test_to_scan
from strapi.send_strapi_info import update_tests_results as strapi_update_tests_results
from utils.locations import results_dir
from logging import log, INFO, ERROR


def update_tests_results(scan_id: int, test_id: int | None, tool: TestTool, tests_results: list[SecurityTest],
                         scan_result: RunScanResult, status: TestStatus) -> list[SecurityTest]:
    if test_id is None:
        new_test = NewSecurityTest(tool=tool,
                                   scan_time=scan_result.scan_time,
                                   command=scan_result.command,
                                   result=scan_result.data,
                                   status=status)
        tests_results.append(new_test)
    else:
        for test in tests_results:
            if test["id"] == test_id:
                test["scan_time"] = scan_result.scan_time
                test["command"] = scan_result.command
                test["result"] = scan_result.data
                test["status"] = status.value

    tests_results = strapi_update_tests_results(scan_id=scan_id, test_results=tests_results)
    log(INFO, f"Added results of {tool.value} test to scan with id: {scan_id}")

    return tests_results


def run_test(scan_id: int, tests_results: list[SecurityTest], scan_tool: ScanTool) -> list[SecurityTest]:
    tool = scan_tool.tool_name()

    log(INFO, f"Starting {tool.value} test")

    try:
        test_id, tests_results = add_test_to_scan(scan_id=scan_id,
                                                  tool=tool,
                                                  current_test_results=tests_results)

        try:
            scan_result = scan_tool.run_scan()
            tests_results = update_tests_results(scan_id, test_id, tool, tests_results, scan_result,
                                                 TestStatus.finished)

        except ScanTestFailed as e:
            log(ERROR, f"Exception occurred while running {tool.value} test. Message: {str(e)}")
            tests_results = update_tests_results(scan_id, test_id, tool, tests_results, scan_result,
                                                 TestStatus.failed)

    except CustomFatalException as e:
        log(ERROR, f"CustomFatalException occurred while running {tool.value} test. Message: {str(e)}")
        raise

    return tests_results


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

    except CustomFatalException as e:
        log(ERROR, f"CustomFatalException occurred: {e}")
