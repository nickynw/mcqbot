"""A logger to use throughout the project"""
import logging
from logging import Logger


def create_logger(name: str) -> Logger:
    """
    Create a custom logger with configurations set to avoid repeating code.

    Args:
        name str: the name of the module the logger is being used in.

    Returns:
        _type_: _description_
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    chandler = logging.StreamHandler()
    chandler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    chandler.setFormatter(formatter)

    logger.addHandler(chandler)

    return logger
