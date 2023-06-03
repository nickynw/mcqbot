"""Module containing utility functions of neo4j database connection"""
# pylint: disable=broad-exception-caught broad-exception-raised
from api.graphs.neo4j_graph import Neo4JGraph
from dotenv import load_dotenv

load_dotenv()


def try_connections():
    """Attempts to find a working URI as the working URI changes between testing environments."""
    output = None
    for uri in [
        'bolt://neo4j:7687',
        'bolt://localhost:7687',
        'bolt://127.0.0.1:7687',
        'bolt://0.0.0.0:7687',
    ]:
        try:
            Neo4JGraph(uri, 'neo4j', 'password')
            output = uri
            print('%s used for working URI.' % uri)
        except Exception:
            print('%s connection failed. Attempting different URI...' % uri)
    if output is None:
        raise Exception('All uri connection attempts failed.')
    return output


URI = try_connections()
