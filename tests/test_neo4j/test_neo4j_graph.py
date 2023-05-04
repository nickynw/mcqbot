"""Test the MCQGraph class object interface with Neo4J Database, are operations working as expected"""
import logging
import os
from typing import Generator

import pytest
from app.data.mcq_graph import MCQGraph
from app.data.neo4j_graph import Neo4JGraph
from app.models import MCQNode
from dotenv import load_dotenv
from tests.test_templates.test_mcq_graph import TestMCQGraph

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)

load_dotenv()
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_password = os.getenv('NEO4J_PASSWORD')


@pytest.fixture(name='graph')
def graph_fixture() -> Generator[MCQGraph, None, None]:
    """
    Creates fixtures MCQGraph object to work with

    Yields:
        Generator[MCQGraph]: MCQGraph object that connects via driver to database.
    """
    graph = Neo4JGraph(neo4j_uri, 'neo4j', neo4j_password)
    yield graph
    graph.delete_all()
    graph.close()


@pytest.fixture(name='single_node_graph')
def single_node_fixture(
    graph: Neo4JGraph,
) -> Generator[MCQGraph, None, None]:
    """
    Creates a single node using the driver directly, rather than calling a function for test purposes.

    Args:
        graph (Generator[MCQGraph]): An empty databases and MCQGraph driver.

    Yields:
        Generator[MCQGraph]: A database populated with sample nodes.
    """
    with graph.driver.session() as session:
        node = {'name': 'Sample Node 0'}
        session.run('CREATE (:Entity $prop)', prop=node)
    yield graph


@pytest.mark.usefixtures('graph', 'single_node_graph', 'complex_graph')
class TestNeo4JGraph:
    """Test class for Neo4JGraph"""

    def test_neo4j_graph(self):
        """Run all the tests in mcq graph template file with these fixtures"""
        TestMCQGraph()
