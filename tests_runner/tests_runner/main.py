from strapi.wapiti_classifications import add_classifications
from utils.log import setup_logger
from logging import log, INFO, ERROR
from runner import run_service

if __name__ == "__main__":
    setup_logger()
    add_classifications()

    try:
        log(INFO, "application started")
        run_service()

    except Exception as e:
        log(ERROR, f"Fatal error occurred while application run. Error: {e}")
