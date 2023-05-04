"""Test the MCQ Generator Class with an Networkx Graph Database"""
import pytest
from app.data.nx_graph import NXGraph
from app.models import MCQ
from app.utils.mcq_generator import MCQGenerator


@pytest.mark.parametrize('test_graph', [NXGraph()], indirect=True)
def test_mcq_generator_with_nx(test_graph):
    """A test to show that the MCQ generator is working correctly."""

    mcq = MCQGenerator(test_graph, seed=2)
    output = mcq.generate()
    assert output == MCQ(
        answer='Greetings',
        topic='Hey',
        choices=['Adios', 'See you later', 'Helyou later', 'Greetings'],
    )
