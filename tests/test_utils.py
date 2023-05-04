# pylint: disable=duplicate-code
"""Provides fixtures shared between different test files."""
from typing import Dict, Generator, List
import pytest
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship

def fill_graph(graph: MCQGraph, data: Dict[str, List[str]]) -> MCQGraph:
    """
    Given a graph, fills it with the provided data.

    Args:
        graph (_type_): input graph
        data (_type_): input data

    Returns:
        _type_: _description_
    """
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
    graph.delete_all()
    graph.create_nodes(nodes=nodes)
    graph.create_relationships(relationships=relationships)
    return graph
