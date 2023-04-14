"""A logger to use throughout the project"""
import logging
from logging import Logger
from typing import Any, Dict

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


def log_query(query: str, **params: Dict[str, Any]) -> str:
    """
    Builds a query string from provided parameters for use in logging.
    E.g. Cypher queries run in sessions.

    Args:
        query (str): the input string to modify

    Returns:
        str: a modified string using input params
    """

    for arg_name, arg_value in params.items():
        query = query.replace(f'${arg_name}', str(arg_value))
    return query
