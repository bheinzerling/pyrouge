import logging


def get_console_logger(name):
    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(logFormatter)
        logger.addHandler(ch)
    return logger


def get_global_console_logger():
    return get_console_logger('global')
