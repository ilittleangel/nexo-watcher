import logging
import logging.handlers

from settings import LOG_LEVEL


def set_log_level(level):
    switcher = {
        "ERROR": logging.ERROR,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "CRITICAL": logging.CRITICAL
    }
    return switcher.get(level.upper(), "Invalid LOG LEVEL")


# noinspection PyShadowingNames
def init_logging(log_file):
    s = f'[%(asctime)s][%(name)s][%(levelname)s]: %(message)s'
    logging.basicConfig(format=s, level=set_log_level(LOG_LEVEL))
    formatter = logging.Formatter(s)

    fh = logging.handlers.TimedRotatingFileHandler(filename=f"{log_file}.log", when='MIDNIGHT', backupCount=7, utc=True)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logging.getLogger('watcher').addHandler(fh)


# noinspection PyShadowingNames
def close_logging():
    for handler in logging.getLogger('watcher').handlers:
        handler.close()
