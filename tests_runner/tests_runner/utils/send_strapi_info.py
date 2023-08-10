from utils.base_requests import update
from schemas.security_scan import TestStatus, SecurityTest, AddSecurityTestResult, TestTool
from exceptions.api import UpdateTestResultsException
from logging import log, INFO, ERROR


def update_test_status(scan_id: int, test_id: int, status: TestStatus,
                       current_test_results: list[SecurityTest]) -> list[SecurityTest]:
    # w podanej liście wyszukuje test o podanym id i podmienia mu status
    # zwraca listę test results z odpowiedzi
    pass


def update_scan_status(id: int, status: TestStatus, error_ms: str | None = None):
    data = {"status": status.value}

    if error_ms is not None:
        data["error_ms"] = error_ms

    try:
        update(f"/page-security-tests/{id}", data)
        log(INFO, f"Successfully updated scan entry. ID: {id}, send_data: {data}")

    except Exception as e:
        log(ERROR, f"Unable to update scan entry with id: {id}. Error: {e}")


def add_test_to_scan(scan_id: int, tool: TestTool,
                     current_test_results: list[SecurityTest]) -> tuple[int, list[SecurityTest]]:
    current_test_results.append({"tool": tool.value, "status": TestStatus.running.value})
    data = {"tests_results": current_test_results}

    response = update(f"/page-security-tests/{scan_id}?populate=tests_results", data)

    if response.status_code == 200:
        response_data = response.json()
        tests_results = response_data["data"]["attributes"]["tests_results"]
        id = tests_results[-1]["id"]

        return (id, tests_results)

    else:
        return (None, current_test_results[:-1])


def update_tests_results(scan_id: int, test_results: list[SecurityTest]) -> list[SecurityTest]:
    data = {"tests_results": test_results}

    response = update(f"/page-security-tests/{scan_id}?populate=tests_results", data)

    if response.status_code == 200:
        response_data = response.json()
        tests_results = response_data["data"]["attributes"]["tests_results"]
        id = tests_results[-1]["id"]

        return tests_results

    else:
        raise UpdateTestResultsException(scan_id=scan_id,
                                         status_code=response.status_code,
                                         message=response.reason)
