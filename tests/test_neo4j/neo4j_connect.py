"""Module containing utility functions of neo4j database connection"""
# pylint: disable=broad-exception-caught broad-exception-raised
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def try_connections():
    """Attempts to find a working URI as the working URI changes between testing environments."""
    uri = None
    try:
        GraphDatabase.driver(
            'bolt://neo4j:7687', auth=('neo4j', os.getenv('NEO4J_PASSWORD'))
        )
        uri = 'bolt://neo4j:7687'
    except Exception:
        print('%s connection failed. Attempting different URI...' % uri)
    try:
        GraphDatabase.driver(
            'bolt://localhost:7687',
            auth=('neo4j', os.getenv('NEO4J_PASSWORD')),
        )
        uri = 'bolt://localhost:7687'
    except Exception:
        print('%s connection failed. Attempting different URI...' % uri)
    try:
        GraphDatabase.driver(
            'bolt://127.0.0.1:7687',
            auth=('neo4j', os.getenv('NEO4J_PASSWORD')),
        )
        uri = 'bolt://127.0.0.1:7687'
    except Exception:
        print('%s connection failed. Attempting different URI...' % uri)
    if uri is None:
        raise Exception('All uri connection attempts failed.')
    print(uri)
    print('__________***_____')
    return uri


URI = try_connections()
