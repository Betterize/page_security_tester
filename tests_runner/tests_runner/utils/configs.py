import os


class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
            cls._instance._REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
            cls._instance._REDIS_QUEUE_NAME = os.environ.get('REDIS_QUEUE_NAME', 'security_tests')
            cls._instance._STRAPI_BASE_URL = os.environ.get('STRAPI_BASE_URL', 'http://127.0.0.1:1337')
            cls._instance._STRAPI_TOKEN = os.environ.get('STRAPI_TOKEN')

        if cls._instance._STRAPI_TOKEN is None:
            raise ValueError("No STRAPI_TOKEN env variable found")

        return cls._instance

    @property
    def REDIS_HOST(self):
        return self._REDIS_HOST

    @property
    def REDIS_PORT(self):
        return self._REDIS_PORT

    @property
    def REDIS_QUEUE_NAME(self):
        return self._REDIS_QUEUE_NAME

    @property
    def STRAPI_BASE_URL(self):
        return self._STRAPI_BASE_URL

    @property
    def STRAPI_TOKEN(self):
        return self._STRAPI_TOKEN
