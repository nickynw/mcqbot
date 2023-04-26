"""Generates a graph from some sample data"""
from typing import Dict, List

import networkx as nx
from app.data.nx_graph import NXGraph
from app.models import MCQNode, MCQRelationship

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


def create_graph() -> nx.DiGraph:
    """
    Creates a network x graph from data.

    Returns:
        nx.DiGraph: a directed graph containing nodes representing units of information
    """
    graph = NXGraph()
    nodes = [MCQNode(**{'name': key}) for key in data]
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
    return graph
