"""Test the Fake Word Generator Class"""
import random

from app.data.neurograph import create_graph
from app.utils.mcq_generator import MCQGenerator


def test_mcq_generator():
    """A test to show that the MCQ generator is working correctly."""
    random.seed(2)
    graph = create_graph()
    mcq = MCQGenerator(graph)
    output = mcq.generate()
    assert output == {
        'answer': 'Glycine',
        'choices': ['Glycine', 'Vitamin C', 'Serodroxytryptophan', 'L-DOPA'],
        'topic': 'Neurotransmitter',
    }
