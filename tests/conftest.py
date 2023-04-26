"""Provides fixtures shared between different test files."""
import pytest
from app.models import MCQNode, MCQRelationship


@pytest.fixture(scope='session', name='mcq_graph')
def mcq_graph(request):
    """Fixture for creating and populating an MCQ Graph"""
    data = {
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
    nodes = [MCQNode(**{'name': key}) for key in data]
    relationships = []
    for key, value in data.items():
        for item in value:
            relationships.append(
                MCQRelationship(
                    **{'start_node': key, 'end_node': item, 'type': 'links_to'}
                )
            )
    graph = request.param
    graph.delete_all()
    graph.create_nodes(nodes=nodes)
    graph.create_relationships(relationships=relationships)
    yield graph
    graph.delete_all()
    graph.close()
