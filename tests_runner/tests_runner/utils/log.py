import os
import pathlib

import logging.config
from logging.handlers import TimedRotatingFileHandler
import datetime
from pythonjsonlogger import jsonlogger

log_directory = 'logs'

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
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


def setup_logger():
    pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(LOGGING_CONFIG)
