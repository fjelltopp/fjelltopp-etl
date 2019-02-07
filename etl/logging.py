import watchtower
import logging
LOGGING_FORMAT = '%(asctime)s - %(levelname)-7s - %(message)s'


def get_logger(log_name: str = __name__,
               level: int=logging.INFO,
               log_group: str="etl") -> logging.Logger:
    logging.basicConfig(level=level, format=LOGGING_FORMAT)
    logger = logging.getLogger(log_name)
    logger.addHandler(watchtower.CloudWatchLogHandler(log_group=log_group))
    return logger

