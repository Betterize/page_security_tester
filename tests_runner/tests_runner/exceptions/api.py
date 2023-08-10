from schemas.security_scan import TestStatus, SecurityTest, TestTool


class UpdateTestResultsException(Exception):

    def __init__(self, scan_id: int, status_code: int, message: str):
        self.scan_id = scan_id
        self.status_code = status_code
        self.message = message

        super().__init__(
            f"Unable to update tests_results of scan with id: {scan_id}. Returned status code: {status_code}, message: {message}"
        )
