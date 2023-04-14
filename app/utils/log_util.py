"""A logger to use throughout the project"""
import logging


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


def session_query(query, **params):
    for arg_name, arg_value in params.items():
        query = query.replace(f'${arg_name}', str(arg_value))
    return query
