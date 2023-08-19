from scan_tools.scan_tool import ScanTool
from exceptions.scan_tools import WapitiJsonDecodingFailed
from schemas.security_scan import TestTool
from enum import Enum
import json


class WapitiScope(Enum):
    page = 'page'
    domain = 'domain'


class WapitiScan(ScanTool):

    def __init__(self, result_directory: str, url: str, scope: WapitiScope = WapitiScope.domain) -> None:
        super().__init__(filename='wapiti.json', result_directory=result_directory, command=[])

        wapiti_command: list[str] = [
            'wapiti', '-u', url, '-f', 'json', '--scope', scope.value, '--no-bugreport', '--flush-session',
            '-o',
            self.result_path()
        ]

        self.command = wapiti_command

    def tool_name(self) -> TestTool:
        return TestTool.wapiti

    def process_result(self):
        try:
            with open(self.result_path()) as json_file:
                data = json.load(json_file)

                if "classifications" in data:
                    del data["classifications"]

            return data

        except json.decoder.JSONDecodeError as e:
            raise WapitiJsonDecodingFailed(message=e.msg, location=self.result_path())
