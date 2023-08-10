from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Service:
    name: str | None
    product: str | None
    version: str | None
    tunnel: str | None
    method: str | None
    conf: str | None
    cpe: str | None


def service_from_dict(data):
    name = data.get("@name")
    product = data.get("@product")
    version = data.get("@version")
    tunnel = data.get("@tunnel")
    method = data.get("@method")
    conf = data.get("@conf")
    cpe = data.get("cpe")

    return Service(name, product, version, tunnel, method, conf, cpe)


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
    service: Service | None
    reason: str | None
    scripts: list[str]


@dataclass_json
@dataclass
class NmapResult:
    host_names: list[HostName] | None
    ports: list[Port] | None
