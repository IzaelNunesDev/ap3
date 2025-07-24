
import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file_handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5)
    log_file_handler.setFormatter(log_formatter)
    log_file_handler.setLevel(logging.INFO)

    log_console_handler = logging.StreamHandler(sys.stdout)
    log_console_handler.setFormatter(log_formatter)
    log_console_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(log_file_handler)
    root_logger.addHandler(log_console_handler)

    logging.getLogger('uvicorn.access').handlers = [log_file_handler, log_console_handler]
    logging.getLogger('uvicorn.error').handlers = [log_file_handler, log_console_handler]
