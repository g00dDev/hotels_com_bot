# -*- coding: utf-8 -*-
import logging.config

logger_main = logging.getLogger('main')
logger_requests = logging.getLogger('http_requests')

ERROR_LOG_FILENAME: str = ".errors.log"
LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {  # The formatter name, it can be anything that I wish
            "format": "%(asctime)s: %(name)s:%(process)d:%(lineno)d   " "%(levelname)s: %(message)s",
            # What to add in the message
            "datefmt": "%Y-%m-%d %H:%M:%S",  # How to display dates
        },
        "simple": {  # The formatter name
            "format": "%(message)s",  # As simple as possible!
        },
        "json": {},
    },
    "handlers": {
        "logfile": {  # The handler name
            "formatter": "default",  # Refer to the formatter defined above
            # "level": "ERROR",  # FILTER: Only ERROR and CRITICAL logs
            "level": "DEBUG",  # FILTER: All logs
            "class": "logging.handlers.RotatingFileHandler",  # OUTPUT: Which class to use
            "filename": ERROR_LOG_FILENAME,  # Param for class above. Defines filename to use, load it from constant
            "maxBytes": 2097152,  # Max size in bytes of a log file
            "backupCount": 2,  # Param for class above. Defines how many log files to keep as it grows
        },
        "verbose_output": {  # The handler name
            "formatter": "default",  # Refer to the formatter defined above
            "level": "DEBUG",  # FILTER: All logs
            "class": "logging.StreamHandler",  # OUTPUT: Which class to use
            "stream": "ext://sys.stdout",  # Param for class above. It means stream to console
        },
        "json": {  # The handler name
            "formatter": "json",  # Refer to the formatter defined above
            "class": "logging.StreamHandler",  # OUTPUT: Same as above, stream to console
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "main": {  # The name of the logger, match module!
            "level": "DEBUG",  # FILTER: only DEBUG logs onwards from logger
            "handlers": [
                "verbose_output",  # Refer the handler defined above
            ],
        },
        "http_requests": {  # The name of the logger, this SHOULD match your module!
            "level": "DEBUG",  # FILTER: only DEBUG logs onwards from logger
            "handlers": [
                "verbose_output",  # Refer the handler defined above
            ],
        },
    },
    "root": {  # All loggers (including tryceratops)
        # "level": "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR" "CRITICAL"
        "level": "INFO",  # FILTER: only INFO logs onwards
        "handlers": [
            "logfile",  # Refer the handler defined above
            "json"  # Refer the handler defined above
        ]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
