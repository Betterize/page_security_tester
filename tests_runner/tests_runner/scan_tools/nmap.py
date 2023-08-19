import xmltodict
from schemas.security_scan import TestTool
from scan_tools.scan_tool import ScanTool
from schemas.nmap import HostName, NmapResult, Port, service_from_dict, NmapResultDict


class NmapScan(ScanTool):

    def __init__(self, result_directory: str, url: str) -> None:
        super().__init__(filename='nmap.xml', result_directory=result_directory, command=[])

        nmap_command: list[str] = [
            'nmap', '-v', '-sC', '-A', '-sV', '--max-retries=1', '-p1-65355', '--host-timeout=720s',
            clean_url(url=url), '-Pn', '-oX',
            self.result_path()
        ]

        # nmap_command: list[str] = ['nmap', clean_url(url=url), '-oX', self.result_path()]

        self.command = nmap_command

    def tool_name(self) -> TestTool:
        return TestTool.nmap

    def process_result(self) -> NmapResultDict:
        with open(self.result_path(), 'r') as xml_file:
            xml_data = xml_file.read()
            self.xml_dict = xmltodict.parse(xml_data)

            return self.select_needed().to_dict()

    def select_needed(self) -> NmapResult:
        if "host" not in self.xml_dict["nmaprun"]:
            # execute if website does not exists
            return NmapResult(host_names=None, ports=None)

        host = self.xml_dict["nmaprun"]["host"]

        host_names: list[HostName] = [
            HostName(name=host["@name"], type=host["@type"]) for host in (host["hostnames"]["hostname"])
        ]

        if "ports" in self.xml_dict["nmaprun"]["host"] and "port" in self.xml_dict["nmaprun"]["host"]["ports"]:
            visible_ports: list[Port] = []

            for port_data in self.xml_dict["nmaprun"]["host"]["ports"]["port"]:
                protocol = port_data["@protocol"]
                id = port_data["@portid"]
                state = port_data["state"]["@state"]
                service = service_from_dict(port_data["service"])
                reason = port_data["state"]["@reason"]

                scripts = []

                if "script" in port_data:
                    if "@id" in port_data["script"]:
                        scripts.append({"id": port_data["script"]["@id"]})
                    else:
                        for script in port_data["script"]:
                            scripts.append(script["@id"])

                visible_ports.append(Port(id, protocol, state, service, reason, scripts))

            return NmapResult(host_names, ports=visible_ports)

        return NmapResult(host_names, ports=None)


def clean_url(url: str) -> str:
    return url.replace("https://", "").replace("http://", "")
