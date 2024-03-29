"""Test the MCQBuilder Class using a Neo4J Graph Database"""
import os
from typing import Generator

import pytest
from app.core.mcq_builder import MCQBuilder
from app.graphs.mcq_graph import MCQGraph
from app.graphs.neo4j_graph import Neo4JGraph
from app.models import MCQ
from tests.test_neo4j.neo4j_connect import URI


@pytest.fixture(name='graph')
def graph_fixture() -> Generator[MCQGraph, None, None]:
    """
    Creates neo4j graph object fixture for tests to work with the mcq generator

    Yields:
        Generator[MCQGraph]: MCQGraph object that connects via driver to database.
    """
    graph = Neo4JGraph(URI, 'neo4j', os.getenv('NEO4J_PASSWORD'))
    yield graph
    graph.delete_all()


@pytest.mark.usefixtures('graph', 'complex_graph')
def test_mcq_generator_with_neo4j(complex_graph):
    """A test to show that the MCQ generator is working correctly."""
    mcq = MCQBuilder(complex_graph, seed=3)
    output = mcq.generate()
    assert output == MCQ(
        answer='See you later',
        topic='Farewells',
        choices=['Wordsla', 'See you later', 'Hey', 'Good Morning'],
    )
