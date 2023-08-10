import subprocess
from enum import Enum
from utils.locations import create_file_with_path
import json


class WapitiScope(Enum):
    page = 'page'
    domain = 'domain'


def run_wapiti(url: str, result_dir: str, scope: WapitiScope = WapitiScope.domain):
    create_file_with_path(f'{result_dir}', 'wapiti.json')
    start_wapiti_test(url=url, scope=scope, filename=f'{result_dir}/wapiti.json')
    return test_result(f'{result_dir}/wapiti.json')


def test_result(path: str):
    with open(path) as json_file:
        data = json.load(json_file)

        if "classifications" in data:
            del data["classifications"]

    return data


def start_wapiti_test(url: str, scope: WapitiScope, filename: str) -> None:
    wapiti_command: list[str] = [
        'wapiti', '-u', url, '-f', 'json', '--scope', scope, '--no-bugreport', '--flush-session', '-o',
        filename
    ]

    try:
        result = subprocess.run(wapiti_command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error occurred while running wapiti test:", e)
