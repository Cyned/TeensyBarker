import logging

from logging.handlers import TimedRotatingFileHandler
from os.path import join as path_join

from app.config import APP_DIR


def create_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s - %(levelname)s %(module)s %(funcName)s] - %(message)s')
    fh = TimedRotatingFileHandler(path_join(APP_DIR, 'logger', 'MAIN.log'), when='midnight', encoding='utf-8')
    fh.suffix = '%Y_%m_%d.log'
    # fh.setLevel(logging.DEBUG)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # ch.setFormatter(formatter)
    # logger.addHandler(ch)

    return logger
