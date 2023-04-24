"""Test the Fake Word Generator Class"""
import random
from typing import Dict, Generator, List

from app.utils.mcq_generator import MCQGenerator
from app.models import MCQ, MCQNode, MCQRelationship
from app.data.nx_graph import NXGraph
from mcq_graph import MCQGraph

data: Dict[str, List[str]] = {
    'Neurotransmitter': [
        'Serotonin',
        'Glycine',
        'Glutamate',
        'GABA',
        'Dopamine',
        'Epinephrine',
    ],
    'Serotonin': [],
    'Glycine': [],
    'Glutamate': [],
    'GABA': [],
    'Epinephrine': [],
    'Dopamine': [],
    'Serine': [],
    'Histadine': [],
    'Amino Acid': ['Glycine', 'Glutamate', 'Serine', 'Histadine'],
    'Monoamine': ['Serotonin', 'Epinephrine', 'Dopamine'],
    'L-tryptophan': ['Serotonin'],
    'L-DOPA': ['Dopamine'],
    '5-hydroxytryptophan': ['Serotonin'],
    'Vitamin C': [
        'Serotonin',
        'L-tryptophan',
        '5-hydroxytryptophan',
        'L-DOPA',
        'Dopamine',
    ],
    'Precursor': ['L-tryptophan', 'L-DOPA', '5-hydroxytryptophan'],
    'GABA Receptor': ['GABA', 'Muscimol'],
    'Muscimol': [],
}

@pytest.fixture(name='graph')
def graph_fixture() -> Generator[MCQGraph, None, None]:
    """
    Creates fixtures MCQGraph object to work with

    Yields:
        Generator[MCQGraph]: MCQGraph object that connects via driver to database.
    """
    graph = NXGraph()
    nodes = [MCQNode(**{'name': key}) for key in data.keys()]
    relationships = []
    for key, value in data.items():
        for item in value:
            relationships.append(
                MCQRelationship(
                    **{'start_node': key, 'end_node': item, 'type': 'links_to'}
                )
            )
    graph.create_nodes(nodes=nodes)
    graph.create_relationships(relationships=relationships)
    yield graph
    graph.delete_all()


def test_mcq_generator(graph):
    """A test to show that the MCQ generator is working correctly."""

    mcq = MCQGenerator(graph, seed=2)
    output = mcq.generate()
    assert output == MCQ(
        answer='Glycine',
        topic='Neurotransmitter',
        choices=['GABA', 'Serotonin', 'Glycine'],
    )
