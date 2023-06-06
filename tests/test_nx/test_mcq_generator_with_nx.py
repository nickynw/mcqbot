"""Test the MCQ Generator Class with an Networkx Graph Database"""
from typing import Generator

import pytest
from api.graphs.mcq_graph import MCQGraph
from api.graphs.nx_graph import NXGraph
from api.models import MCQ
from api.utils.mcq_generator import MCQGenerator


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


@pytest.mark.usefixtures('graph', 'complex_graph')
def test_mcq_generator_with_nx(complex_graph):
    """A test to show that the MCQ generator is working correctly."""

    mcq = MCQGenerator(complex_graph, seed=3)
    output = mcq.generate()
    assert output == MCQ(
        answer='Hola',
        topic='Greetings',
        choices=['Wordsyou later', 'Hola', 'Goodbye', 'Blah'],
    )
