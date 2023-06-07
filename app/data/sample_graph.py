# pylint: disable=duplicate-code
"""Provides a sample graph for use in the main app."""
from typing import Dict, List

from app.graphs.nx_graph import NXGraph


def generate_graph() -> NXGraph:
    """Provides a sample graph to use."""
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
    graph = NXGraph()
    graph.fill_graph(data)
    return graph
