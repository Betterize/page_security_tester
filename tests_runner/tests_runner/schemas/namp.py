from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class HostName:
    name: str
    type: str


@dataclass_json
@dataclass
class Port:
    id: int
    protocol: str
    state: str
    service: 'typing.Any'
    reason: str
    scripts: list[str]


@dataclass_json
@dataclass
class NmapResult:
    host_names: list[HostName]
    ports: list[Port]
