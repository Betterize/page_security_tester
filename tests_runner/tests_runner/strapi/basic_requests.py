import requests
from configs import Configuration

config = Configuration()

headers = {'Authorization': f'Bearer {config.STRAPI_TOKEN}'}

rest_api_url = f"{config.STRAPI_BASE_URL}/api"


def update(endpoint: str, data: dict):
    response = requests.put(f"{rest_api_url}{endpoint}", json={"data": data}, headers=headers)

    return response


def get(endpoint: str):
    response = requests.get(f"{rest_api_url}{endpoint}", headers=headers)

    return response


def create(endpoint: str, data: dict):
    response = requests.post(f"{rest_api_url}{endpoint}", json={"data": data}, headers=headers)

    return response