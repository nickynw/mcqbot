"""Module containing utility functions of neo4j database connection"""
# pylint: disable=broad-exception-caught broad-exception-raised
from api.data.neo4j_graph import Neo4JGraph
from dotenv import load_dotenv

load_dotenv()


def try_connections():
    """Attempts to find a working URI as the working URI changes between testing environments."""
    uri = None
    try:
        uri = 'bolt://neo4j:7687'
        Neo4JGraph(uri, 'neo4j', 'password')
    except Exception:
        print('%s connection failed. Attempting different URI...' % uri)
    try:

        uri = 'bolt://localhost:7687'
        Neo4JGraph(uri, 'neo4j', 'password')
    except Exception:
        print('%s connection failed. Attempting different URI...' % uri)
    try:
        uri = 'bolt://127.0.0.1:7687'
        Neo4JGraph(uri, 'neo4j', 'password')
    except Exception:
        print('%s connection failed. Attempting different URI...' % uri)
    if uri is None:
        raise Exception('All uri connection attempts failed.')
    return uri


URI = try_connections()
