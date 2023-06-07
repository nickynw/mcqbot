"""Test the MCQ Generator Class with an Networkx Graph Database"""
from typing import Generator

import pytest
from app.core.mcq_generator import MCQGenerator
from app.graphs.mcq_graph import MCQGraph
from app.graphs.nx_graph import NXGraph
from app.models import MCQ


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
