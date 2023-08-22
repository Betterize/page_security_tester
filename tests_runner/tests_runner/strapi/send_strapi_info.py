from strapi.basic_requests import update
from schemas.security_scan import TestStatus, SecurityTest, TestTool
from logging import log, INFO, ERROR


def update_scan_status(id: int, status: TestStatus, error_ms: str | None = None):
    data = {"status": status.value}

    if error_ms is not None:
        data["error_ms"] = error_ms

    unused = update(f"/page-security-tests/{id}", data)
    log(INFO, f"Successfully updated scan entry. ID: {id}, send_data: {data}")


def add_test_to_scan(scan_id: int, tool: TestTool,
                     current_test_results: list[SecurityTest]) -> tuple[int, list[SecurityTest]]:
    current_test_results.append({"tool": tool.value, "status": TestStatus.running.value})
    data = {"tests_results": current_test_results}

    response = update(f"/page-security-tests/{scan_id}?populate=tests_results", data)

    response_data = response.json()
    tests_results = response_data["data"]["attributes"]["tests_results"]
    id = tests_results[-1]["id"]

    return (id, tests_results)


def update_tests_results(scan_id: int, test_results: list[SecurityTest]) -> list[SecurityTest]:
    data = {"tests_results": test_results}

    response = update(f"/page-security-tests/{scan_id}?populate=tests_results", data)

    response_data = response.json()
    tests_results = response_data["data"]["attributes"]["tests_results"]

    return tests_results
