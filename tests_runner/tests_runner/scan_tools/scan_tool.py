import subprocess
from utils.locations import create_file_with_path
from exceptions.scan_tools import MethodNotImplemented, ScanTestFailed
from schemas.security_scan import TestTool, RunScanResult
from schemas.nmap import NmapResultDict
from schemas.wapiti import WapitiResult
from typing import Union
import time
from logging import log, INFO


class ScanTool:
    filename: str
    result_directory: str
    command: list[str]

    def __init__(self, filename: str, result_directory: str, command: list[str]) -> None:
        self.filename = filename
        self.result_directory = result_directory
        self.command = command

    def run_scan(self) -> RunScanResult:
        create_file_with_path(f'{self.result_directory}', self.filename)

        start_time = time.time()

        self.scan()
        final_result = self.process_result()

        scan_time = "{:.2f}".format(time.time() - start_time)

        log(INFO, f"Finished {self.tool_name().value} test after {scan_time}s")

        return RunScanResult(command=" ".join(self.command), data=final_result, scan_time=scan_time)

    def process_result(self) -> Union[NmapResultDict, WapitiResult]:
        raise MethodNotImplemented(method="process_result")

    def tool_name(self) -> TestTool:
        raise MethodNotImplemented(method="process_result")

    def scan(self) -> None:
        try:
            result = subprocess.run(self.command, capture_output=True, text=True, check=True)

            if (result.stderr is not None) and (not result.stderr == ""):
                raise ScanTestFailed(message=result.stderr, command=self.command)

        except subprocess.CalledProcessError as e:
            raise ScanTestFailed(message=e.stderr)

    def result_path(self) -> str:
        return f'{self.result_directory}/{self.filename}'
