# pylint: disable=duplicate-code
"""Provides a sample graph for use in the main app."""
from api.graphs.nx_graph import NXGraph
from api.models import MCQNode, MCQRelationship


def new_graph() -> NXGraph:
    """Provides a sample graph to use."""
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
        if isinstance(value, list):
            for item in value:
                relationships.append(
                    MCQRelationship(
                        **{
                            'answer_node': key,
                            'topic_node': item,
                            'type': 'includes',
                        }
                    )
                )
                relationships.append(
                    MCQRelationship(
                        **{
                            'topic_node': key,
                            'answer_node': item,
                            'type': 'belongs_to',
                        }
                    )
                )
    graph = NXGraph()
    graph.create_nodes(nodes=nodes)
    graph.create_relationships(relationships=relationships)
    return graph
