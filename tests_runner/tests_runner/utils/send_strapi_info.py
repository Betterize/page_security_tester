from utils.base_requests import update
from schemas.security_scan import TestStatus, SecurityTest, AddSecurityTestResult, TestTool
from logging import log, INFO, ERROR


def update_test_status(scan_id: int, test_id: int, status: TestStatus, current_test_results: list[SecurityTest]) -> list[SecurityTest]:
    # w podanej liście wyszukuje test o podanym id i podmienia mu status
    # zwraca listę test results z odpowiedzi
    pass


def update_scan_status(id: int, status: TestStatus, error_ms: str | None = None):
    data = {"status": status.value}

    if error_ms is not None:
        data["error_ms"] = error_ms

    try:
        update(f"/page-security-tests/{id}", data)
        log(INFO, f"Successfully updated entry. ID: {id}, send_data: {data}")

    except Exception as e:
        log(ERROR, f"Unable to update entry with id: {id}. Error: {e}")


def add_test_to_scan(scan_id: int, tool: TestTool, current_test_results: list[SecurityTest]) -> tuple[int, list[SecurityTest]]:
    data = {"tests_results": current_test_results.append()}

    # do tabliczy test results dodaje na ostanie miejsce {"tool": tool, "status": running}
    # z wyniku bierze tablice tests_results i pobiera z niej ostatnią wartość
        # id tej wartości to id nowo dodanego kontenera
        # zwraca krotke (id, lista)

    response = update(f"/page-security-tests/{id}?populate=tests_results", data)

    print(response)