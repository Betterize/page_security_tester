from utils.base_requests import update
from schemas.security_scan import TestStatus

def update_test_status():
    pass


def update_scan_status(id: int, status: TestStatus):
    update(f"/page-security-tests/{id}", {"status": status.value})