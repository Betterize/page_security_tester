from wapiti import run_wapiti
from namp import run_namp
from utils.locations import test_results_dir
from utils.configs import Configuration
import time
import redis


def run_tests(url: str):
    result_dir = test_results_dir(url)

    print("--------------------------")
    print("--- Starts wapiti scan ---")

    wapiti_result = run_wapiti(url=url, result_dir=result_dir, scope="domain")

    print("wapiti results: ")
    print(wapiti_result)

    print("--------------------------")
    print("--- Starts nmap scan ---")

    nmap_result = run_namp(url=url, result_dir=result_dir)

    print("nmap results: ")
    print(nmap_result.to_json())


def run_service():
    config = Configuration()
    print("loaded config")

    redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    print("created redis connection")

    while True:
        print("starting reading from queue...")
        _, message = redis_client.brpop(config.REDIS_QUEUE_NAME)
        decoded_message = message.decode('utf-8')
        print(f"Odczytano wiadomość z kolejki: {decoded_message}")

        if decoded_message == "quit":
            print("Exit triggered by quit message")
            return
        
        run_tests(url=decoded_message)


if __name__ == "__main__":
    print("--- Test started ---")
    start_time = time.time()
    run_service()
    print("--- %s seconds ---" % (time.time() - start_time))
