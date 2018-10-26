import watchtower
import logging

def get_logger(log_name: str = __name__,
               level: int=logging.INFO,
               log_group: str="etl") -> logging.Logger:
    logging.basicConfig(level=level)
    logger = logging.getLogger(log_name)
    logger.addHandler(watchtower.CloudWatchLogHandler(log_group=log_group))
    return logger

