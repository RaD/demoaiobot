import logging
from logging.handlers import SysLogHandler


def get_logger(key: str='demo', level: str='DEBUG', use_syslog: bool=False):
    if hasattr(get_logger, key):
        return getattr(get_logger, key)

    level = getattr(logging, level)

    tpl = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
    formatter = logging.Formatter(tpl)
    handler_console = logging.StreamHandler()
    handler_console.setLevel(level)
    handler_console.setFormatter(formatter)
    logger = logging.getLogger(key)
    logger.setLevel(level)
    logger.addHandler(handler_console)

    if use_syslog:
        handler_syslog = SysLogHandler()
        handler_syslog.setLevel(level)
        handler_syslog.setFormatter(formatter)
        logger.addHandler(handler_syslog)

    setattr(get_logger, key, logger)
    return logger
