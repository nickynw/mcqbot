"""Test the Fake Word Generator Class"""
import random
from typing import Dict, List

from app.utils.mcq_generator import MCQGenerator
from app.models import MCQ, MCQNode, MCQRelationship
from app.data.nx_graph import NXGraph
import logging
import os
from typing import Generator

import pytest
from app.data.mcq_graph import MCQGraph
from app.data.neo4j_graph import Neo4JGraph
from app.models import MCQNode
from dotenv import load_dotenv


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
    load_dotenv()
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    graph = Neo4JGraph(neo4j_uri, 'neo4j', neo4j_password)
    graph.delete_all()
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
    graph.close()


def test_mcq_generator(graph, monkeypatch):
    """A test to show that the MCQ generator is working correctly."""
    # def mock_random_relationship(*args, **kwargs):
    #    return MCQRelationship(start_node='Neurotransmitter', type='links_to', end_node='Serotonin')
    mcq = MCQGenerator(graph, seed=3)
    # monkeypatch.setattr(mcq.graph, 'random_relationship', mock_random_relationship)
    output = mcq.generate()
    assert output == MCQ(
        answer='GABA',
        topic='GABA Receptor',
        choices=['Muscimine', 'GABA', 'Vitamin C', 'Glutamate'],
    )
