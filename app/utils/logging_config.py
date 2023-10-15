import logging
import logging.config
import os

def configure_logging():
    # Default log level is INFO
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'
            },
            'error': {
                'format': '[%(asctime)s] [%(name)s] [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s'
            }
        },
        'handlers': {
            'console_info': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'detailed',
                'stream': 'ext://sys.stdout',
            },
            'console_error': {
                'class': 'logging.StreamHandler',
                'level': 'ERROR',
                'formatter': 'error',
                'stream': 'ext://sys.stderr',
            }
        },
        'loggers': {
            '': {  # root logger
                'level': log_level,
                'handlers': ['console_info', 'console_error'],
            },
        }
    })
