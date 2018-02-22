import queue
import logging
import logging.handlers

from toolbox.conf_loader import RootConfiguration

conf = RootConfiguration()

LOG_LEVEL = logging.INFO

log_formatter = conf.get('logFormatter')
log_queue = queue.Queue(-1)
queue_handler = logging.handlers.QueueHandler(log_queue)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(log_formatter)
file_handler = logging.FileHandler(conf.get('logFilePath'))
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(log_formatter)
stream_queue_listener = logging.handlers.QueueListener(log_queue, stream_handler)
file_queue_listener = logging.handlers.QueueListener(log_queue, file_handler)
stream_queue_listener.start()
file_queue_listener.start()

logger = logging.getLogger(__name__)
logger.addHandler(queue_handler)
logger.setLevel(LOG_LEVEL)
