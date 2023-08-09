import requests
from utils.configs import Configuration

config = Configuration()

headers = {
    'Authorization': f'Bearer {config.STRAPI_TOKEN}'
}

rest_api_url = f"{config.STRAPI_BASE_URL}/api"


def update(endpoint: str, data: dict):
    response = requests.put(f"{rest_api_url}{endpoint}", json={"data": data}, headers=headers)

    if response.status_code == 200:
        print('Zapytanie zostało wysłane pomyślnie.')
    else:
        print('Wystąpił błąd. Kod odpowiedzi:', response.status_code)
        print('Treść odpowiedzi:', response.text)


def get(endpoint: str):
    response = requests.get(f"{rest_api_url}{endpoint}", headers=headers)

    if response.status_code == 200:
        print('Zapytanie zostało wysłane pomyślnie.')
        print(response.json())
    else:
        print('Wystąpił błąd. Kod odpowiedzi:', response.status_code)
        print('Treść odpowiedzi:', response.text)