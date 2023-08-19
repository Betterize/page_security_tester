from typing import TypedDict, Any


class WapitiResult(TypedDict):
    infos: Any
    anomalies: Any
    additionals: Any
    vulnerabilities: Any
