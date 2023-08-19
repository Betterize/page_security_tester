class MethodNotImplemented(Exception):

    def __init__(self, method: str):
        self.method: str = method
        self.message = f"It seems that your class not implement parent class method: {method}"

        super().__init__(self.message)


class ScanTestFailed(Exception):

    def __init__(self, message: str, command: list[str] | None = None):
        self.message = f"Scan test failed with error: {message}"
        self.command = command

        super().__init__(self.message)


class WapitiJsonDecodingFailed(Exception):

    def __init__(self, message: str, location: str):
        self.message = f"Unable to decode body of file: {location}. Error: {message}"

        super().__init__(self.message)
