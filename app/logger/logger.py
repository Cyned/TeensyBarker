import logging

from os.path import join as path_join
from app.config import APP_DIR


def create_logger(file_name: str):
    """
    Create basic logger
    :param file_name: name of log file
    :return: logger
    """
    logger = logging.getLogger(name=file_name)

    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    # create a file and Stream handlers
    fh = logging.FileHandler(filename=path_join(APP_DIR, 'logger', f'{file_name}.log'), mode='a', encoding='utf-8')
    ch = logging.StreamHandler()
    fh.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s %(module)s %(funcName)s] - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def create_collection_logger():
    """ Create logger for the collection part """
    return create_logger('collect')


def create_parser_logger():
    """ Create logger for parser part """
    return create_logger('parser')


def create_app_logger():
    """ Create logger for application """
    return create_logger('application')


def create_basic_logger():
    """ Create logger for all other stuff """
    return create_logger('low_priority')
