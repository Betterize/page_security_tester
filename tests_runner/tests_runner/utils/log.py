import os
import pathlib
from config import Configuration
import logging.config
from logging.handlers import TimedRotatingFileHandler
import datetime
from pythonjsonlogger import jsonlogger

log_directory = 'logs'

config = Configuration()

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': jsonlogger.JsonFormatter,
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(log_directory, f'app_{datetime.datetime.now():%Y-%m-%d}.log'),
            'when': 'midnight',
            'interval': 1,
            'backupCount': 30,
            'encoding': 'utf-8',
            'formatter': 'json',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': config.LOG_LEVEL,
            'propagate': True,
        },
    },
}


def setup_logger():
    pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(LOGGING_CONFIG)
