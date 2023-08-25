from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum
from schemas.nmap import NmapResultDict
from schemas.wapiti import WapitiResult
from typing import Union


@dataclass_json
@dataclass
class ScanStatus(Enum):
    waiting = 'waiting'
    running = 'running'
    finished = 'finished'
    failed = 'failed'


@dataclass_json
@dataclass
class TestStatus(Enum):
    waiting = 'waiting'
    running = 'running'
    finished = 'finished'
    failed = 'failed'


@dataclass_json
@dataclass
class TestTool(Enum):
    wapiti = 'wapiti'
    nmap = 'nmap'


@dataclass_json
@dataclass
class NewSecurityTest:
    tool: TestTool
    scan_time: str | None
    command: str | None
    result: 'typing.Any'
    status: TestStatus


@dataclass_json
@dataclass
class SecurityTest(NewSecurityTest):
    id: int


@dataclass_json
@dataclass
class AddSecurityTestResult:
    new_test_id: int
    tests_results: list[SecurityTest]


@dataclass_json
@dataclass
class SecurityScanAttributes:
    accepted_regulations: bool
    website: str
    email: str
    createdAt: str
    updatedAt: str
    error_msg: str | None
    status: str
    tests_results: list[SecurityTest]


@dataclass_json
@dataclass
class SecurityScan:
    id: int
    attributes: SecurityScanAttributes


@dataclass_json
@dataclass
class SecurityScanRequest:
    id: int
    website: str


@dataclass_json
@dataclass
class NewWapitiClassification:
    name: str
    description: str
    solution: str
    references: dict
    wstg: list[str]


@dataclass
class RunScanResult:
    command: str
    data: Union[NmapResultDict, WapitiResult]
    scan_time: str
