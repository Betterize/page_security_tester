from utils.base_requests import get, create
from schemas.security_scan import NewWapitiClassification
from logging import log, INFO, ERROR
import json


def does_classifications_exists() -> bool:
    response = get(endpoint="/wapiti-classifications")
    return len(response.json()["data"]) > 0


def add_classification_to_strapi(data: NewWapitiClassification):
    response = create(endpoint="/wapiti-classifications", data=data)
    print(f"status code: {response.status_code}")
    print(response.reason)


def add_classifications():
    if not does_classifications_exists():
        log(INFO, "Starting adding classifications data to strapi")
        with open("wapiti_classifications.json", 'r') as file:
            classifications = json.load(file)

            for key, value in classifications.items():
                try:
                    add_classification_to_strapi(
                        NewWapitiClassification(name=key,
                                                description=value["desc"],
                                                solution=value["sol"],
                                                references=value["ref"],
                                                wstg=value["wstg"]).to_dict())

                except Exception as e:
                    log(ERROR, f"Unable to add classification data with key: {key}: {str(e)}")
                    raise e

            log(INFO, "Finished adding classifications data to strapi")

    else:
        log(INFO, "Wapiti classifications data already loaded")
