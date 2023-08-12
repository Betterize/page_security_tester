from dataclasses import dataclass
from dataclasses_json import dataclass_json
from enum import Enum


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
    is_public: bool
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