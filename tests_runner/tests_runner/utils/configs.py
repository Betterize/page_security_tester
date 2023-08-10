import os


class Configuration:

    def __init__(self):
        self.REDIS_HOST = os.environ.get('ENVIRONMENT', '127.0.0.1')
        self.REDIS_PORT = os.environ.get('ENVIRONMENT', '6379')
        self.REDIS_QUEUE_NAME = os.environ.get('REDIS_QUEUE_NAME', 'security_tests')
        self.STRAPI_BASE_URL = os.environ.get('STRAPI_BASE_URL', 'http://127.0.0.1:1337')
        self.STRAPI_TOKEN = os.environ.get('STRAPI_TOKEN')

        if self.STRAPI_TOKEN is None:
            print("Error! No STRAPI_TOKEN found")