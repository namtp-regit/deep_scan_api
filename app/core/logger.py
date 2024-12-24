import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

# create folder logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# create file log with datetime
LOG_FILE = os.path.join(LOG_DIR, f"app_{datetime.datetime.now().strftime('%Y-%m-%d')}.log")


# config logging
def setup_logger():
    logger = logging.getLogger("fastapi_logger")
    logger.setLevel(logging.INFO)

    # create handler write log file
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.INFO)

    # format log
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    # show console.log
    # stream_handler = logging.StreamHandler()
    # stream_handler.setLevel(logging.INFO)
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)

    # add handler to logger
    logger.addHandler(file_handler)

    return logger


# create logger global
logger = setup_logger()
