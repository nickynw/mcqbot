"""Test the MCQ Generator Class with an Networkx Graph Database"""
import pytest
from app.data.nx_graph import NXGraph
from app.models import MCQ
from app.utils.mcq_generator import MCQGenerator


@pytest.mark.parametrize('mcq_graph', [NXGraph()], indirect=True)
def test_mcq_generator(mcq_graph):
    """A test to show that the MCQ generator is working correctly."""

    mcq = MCQGenerator(mcq_graph, seed=2)
    output = mcq.generate()
    assert output == MCQ(
        answer='Glycine',
        topic='Neurotransmitter',
        choices=['GABA', 'Serotonin', 'Glycine'],
    )
