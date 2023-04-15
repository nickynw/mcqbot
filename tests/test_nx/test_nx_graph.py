"""Test the MCQGraph class object interface with Neo4J Database, are operations working as expected"""
import logging
from typing import Generator

import pytest
from app.data.mcq_graph import MCQGraph
from app.data.nx_graph import NXGraph
from app.models import MCQNode
from tests.test_templates.test_mcq_graph import TestMCQGraph

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)

sample_properties = [{'name': 'Sample Node 1'}, {'name': 'Sample Node 2'}]


@pytest.fixture(name='graph')
def graph_fixture() -> Generator[MCQGraph, None, None]:
    """
    Creates fixtures MCQGraph object to work with

    Yields:
        Generator[MCQGraph]: MCQGraph object that connects via driver to database.
    """
    graph = NXGraph()
    yield graph
    graph.delete_all()


@pytest.fixture(name='sample_graph')
def sample_graph_fixture(graph: MCQGraph) -> Generator[MCQGraph, None, None]:
    """
    Populates the database with sample nodes.

    Args:
        graph (Generator[MCQGraph]): An empty databases and MCQGraph driver.

    Yields:
        Generator[MCQGraph]: A database populated with sample nodes.
    """
    graph.create_nodes([MCQNode(**node) for node in sample_properties])
    yield graph


@pytest.fixture(name='single_node_graph')
def single_node_graph_fixture(
    graph: NXGraph,
) -> Generator[MCQGraph, None, None]:
    """
    Creates fixtures MCQGraph object to work with

    Yields:
        Generator[MCQGraph]: MCQGraph object that connects via driver to database.
    """
    graph.graph.add_node('Sample Node 0', name='Sample Node 0')
    yield graph


@pytest.mark.usefixtures('graph', 'sample_graph', 'single_node_graph')
class TestNXGraph:
    """Test class for MCQGraph"""

    def test_mcq_graph(self):
        """Run all the tests in mcq graph template file with these fixtures"""
        TestMCQGraph()
