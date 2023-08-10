import subprocess
from utils.locations import create_file_with_path
from schemas.namp import HostName, NmapResult, Port
import xmltodict


def run_namp(url: str, result_dir: str):
    create_file_with_path(f'{result_dir}', 'nmap.xml')
    start_nmap_test(url=url, filename=f'{result_dir}/nmap.xml')
    final_result = process_result(f'{result_dir}/nmap.xml')

    return final_result


def start_nmap_test(url: str, filename: str) -> None:
    nmap_command: list[str] = [
        'nmap', '-v', '-sC', '-A', '-sV', '--max-retries=1', '-p1-65355', '--host-timeout=720s',
        url.replace("https://", "").replace("http://", ""), '-Pn', '-oX', filename
    ]

    try:
        result = subprocess.run(nmap_command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error occurred while running nmap scan:", e)


def process_result(filename: str) -> NmapResult:
    with open(filename, 'r') as xml_file:
        xml_data = xml_file.read()
        xml_dict = xmltodict.parse(xml_data)

        return select_needed(xml_dict=xml_dict)


def select_needed(xml_dict) -> NmapResult:
    if "host" not in xml_dict["nmaprun"]:
        # execute if website does not exists
        return NmapResult(host_names=None, ports=None)

    host = xml_dict["nmaprun"]["host"]

    host_names: list[HostName] = [
        HostName(name=host["@name"], type=host["@type"]) for host in (host["hostnames"]["hostname"])
    ]

    if "ports" in xml_dict["nmaprun"]["host"]:
        visible_ports: list[Port] = []

        for port_data in xml_dict["nmaprun"]["host"]["ports"]["port"]:
            protocol = port_data["@protocol"]
            id = port_data["@portid"]
            state = port_data["state"]["@state"]
            service = port_data["service"]
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
