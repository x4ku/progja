import logging
import os


level = os.getenv('LOG_LEVEL', logging.INFO)
format = (
    '[%(levelname)s] %(asctime)s '
    '(%(module)s:%(funcName)s:%(lineno)s) '
    '%(message)s'
)


def configure_logging():
    logging.basicConfig(level=level, format=format)
