import logging
import sys
from functools import lru_cache


@lru_cache(maxsize=1)
def configure_logging(log_name=__name__, log_level=logging.INFO):

    formatter = logging.Formatter('[%(asctime)s] [%(threadName)s] [%(levelname)s] %(message)s')
    h_screen = logging.StreamHandler(sys.stdout)

    root_logger = logging.getLogger()
    root_logger.addHandler(h_screen)
    root_logger.setLevel(log_level)
    h_screen.setFormatter(formatter)

    logging.getLogger(log_name).debug(f'"{log_name}" loggers configured')
