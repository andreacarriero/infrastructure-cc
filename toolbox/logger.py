import logging

from toolbox.conf_loader import RootConfiguration

conf = RootConfiguration()

LOG_LEVEL = logging.INFO

logging.basicConfig(
    format = conf.get('logFormatter'),
    level = LOG_LEVEL
)

def get_logger(module_name):
    logger = logging.getLogger(module_name)
    return logger
