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
            'Norepinephrine',
            'ATP',
            'GTP',
            'Nitric Oxide',
            'Acetylcholine',
            'Endocannibinoids',
            'Anandamide',
        ],
        'Endocannibinoids': ['Anandamide'],
        'Acetylcholine': ['Tyrosine', 'acetylCoA', 'Acetate'],
        'Amino Acid': [
            'Glycine',
            'Glutamate',
            'Serine',
            'Histadine',
            'Tyrosine',
            'Phenylalanine',
        ],
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
        'Precursor': [
            'L-tryptophan',
            'L-DOPA',
            '5-hydroxytryptophan',
            'Tyrosine',
        ],
        'GABA Receptor': ['GABA', 'Muscimol'],
        'NMDA Receptor': ['Glutamate', 'NMDA', 'Ketamine', 'Glycine'],
        'AMPA Receptor': ['AMPA', 'Glutamate', 'Perampanel'],
        'Muscarinic Receptor': ['Acetylcholine', 'Muscarine', 'Scopolamine'],
        'Kainate Receptor': ['Kainate', 'UBP-302'],
        'Purines': ['ATP', 'GTP'],
    }
    graph = NXGraph()
    graph.fill_graph(data)
    return graph
