import logging

from toolbox.conf_loader import RootConfiguration
from toolbox.logger import get_logger

conf = RootConfiguration()
log = get_logger(__name__)

log.info("Starting root app...")