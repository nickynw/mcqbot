"""Test the MCQGraph class object interface with Neo4J Database, are operations working as expected"""
import logging
from typing import Generator

import pytest
from api.data.mcq_graph import MCQGraph
from api.data.nx_graph import NXGraph
from tests.test_templates.test_mcq_graph import TestMCQGraph

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)


@pytest.fixture(name='graph')
def graph_fixture() -> Generator[MCQGraph, None, None]:
    """
    Creates a networkx graph fixture for use in testing

    Yields:
        Generator[MCQGraph]: MCQGraph object that connects via driver to database.
    """
    graph = NXGraph()
    yield graph
    graph.delete_all()


@pytest.fixture(name='single_node_graph')
def single_node_fixture(
    graph: NXGraph,
) -> Generator[MCQGraph, None, None]:
    """
    Creates a single node within a networkx x graph without calling the driver function.

    Yields:
        Generator[MCQGraph]: MCQGraph object that connects via driver to database.
    """
    graph.graph.add_node('Sample Node 0', name='Sample Node 0')
    yield graph


@pytest.mark.usefixtures('graph', 'single_node_graph', 'complex_graph')
class TestNXGraph:
    """Test class for NXGraph"""

    def test_nx_graph(self):
        """Run all the tests in mcq graph template file with these fixtures"""
        TestMCQGraph()
