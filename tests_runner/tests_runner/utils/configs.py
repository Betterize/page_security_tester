import os

class Configuration:
    
    def __init__(self):
        self.REDIS_HOST = os.environ.get('ENVIRONMENT', '127.0.0.1')
        self.REDIS_PORT = os.environ.get('ENVIRONMENT', '6379')
        self.REDIS_QUEUE_NAME = os.environ.get('REDIS_QUEUE_NAME', 'security_tests')
