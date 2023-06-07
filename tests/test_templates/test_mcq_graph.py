"""A template to test that all of the MCQGraph class object interface operations working as expected"""
import logging
from typing import Dict, List

import pytest
from api.graphs.mcq_graph import MCQGraph
from api.models import MCQNode, MCQRelationship

pytestmark = pytest.mark.skip(
    reason='This module is not meant to be run directly, it is a template.'
)

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)


class TestMCQGraph:
    """
    Test class for MCQGraph Base Class containing tests to run on all extending classes.

    The following fixtures are provided by extending classes:
        - graph (empty graph)
        - single_node_graph (graph with a single node created directly)

    Uses the following fixtures from conftest:
        - simple_properties (two simple node properties)
        - simple_graph (filled with 2 simple nodes)
        - simple_relationships_graph (filled with 2 simple nodes + two relationships between them)
        - complex_graph (filled with many nodes and relationships)
    """

    def test_get_node(self, single_node_graph: MCQGraph):
        """
        Tests whether the get_node function can successfully get a node from a populated graph.
        The single_node_graph fixture is populated directly without using the create_node function.
        """
        assert single_node_graph.get_node('Sample Node 0')

    def test_create_nodes(
        self, graph: MCQGraph, simple_properties: List[Dict[str, str]]
    ):
        """
        Using a provided list of node properties, test creation of two new nodes in an empty graph,
        and check they now exist using the get_node function.
        """
        graph.create_nodes([MCQNode(**node) for node in simple_properties])
        for properties in simple_properties:
            assert graph.get_node(properties['name']) == MCQNode(**properties)

    def test_delete_all(
        self, simple_graph: MCQGraph, simple_properties: List[Dict[str, str]]
    ):
        """Tests if the delete_all function succesfully deletes the nodes in a populated graph."""
        for properties in simple_properties:
            assert simple_graph.get_node(properties['name']) == MCQNode(
                **properties
            )
        simple_graph.delete_all()
        for properties in simple_properties:
            assert simple_graph.get_node(properties['name']) is None

    def test_duplicate_input(self, graph: MCQGraph):
        """Tests if an error is raised when duplicated properties are used to create nodes in an empty graph."""
        duplicate_properties = [
            {'name': 'Sample Node 1'},
            {'name': 'Sample Node 2'},
            {'name': 'Sample Node 2'},
        ]
        with pytest.raises(ValueError):
            graph.create_nodes(
                [MCQNode(**node) for node in duplicate_properties]
            )

    def test_duplicate_creation(self, simple_graph: MCQGraph):
        """Tests if an error is raised when creating a node that already exists in a populated graph."""
        duplicate_properties = [{'name': 'Sample Node 2'}]
        with pytest.raises(ValueError):
            simple_graph.create_nodes(
                [MCQNode(**node) for node in duplicate_properties]
            )

    def test_relationships(self, simple_graph: MCQGraph):
        """Tests if a new relationship is created in a populated graph without prior relationships."""
        relationship = MCQRelationship(
            **{
                'answer_node': 'Sample Node 1',
                'type': 'is_linked_to',
                'topic_node': 'Sample Node 2',
            }
        )
        assert simple_graph.has_relationship(relationship) is False
        simple_graph.create_relationships([relationship])
        assert simple_graph.has_relationship(relationship) is True

    def test_random_relationship(self, simple_relationships_graph: MCQGraph):
        """Tests retrieval of two random relationships with different seeds."""
        assert simple_relationships_graph.random_relationship(
            seed=1
        ) == MCQRelationship(
            **{
                'answer_node': 'Sample Node 1',
                'type': 'is_linked_to',
                'topic_node': 'Sample Node 2',
            }
        )
        assert simple_relationships_graph.random_relationship(
            seed=5
        ) == MCQRelationship(
            **{
                'answer_node': 'Sample Node 2',
                'type': 'is_linked_to',
                'topic_node': 'Sample Node 1',
            }
        )

    def test_connected_nodes(self, complex_graph: MCQGraph):
        """Tests the retrieval of all nodes connected to a specified node."""

        connected_nodes = sorted(
            complex_graph.connected_nodes(MCQNode(**{'name': 'Hello'}))
        )
        assert connected_nodes == [
            MCQNode(name='English', info=''),
            MCQNode(name='Greetings', info=''),
            MCQNode(name='Words', info=''),
        ]

    def test_related_nodes(self, complex_graph: MCQGraph):
        """Tests the retrieval of related nodes that share the same relationship to a node."""
        related_nodes = sorted(
            complex_graph.related_nodes(
                MCQRelationship(
                    **{
                        'answer_node': 'Hello',
                        'type': 'belongs_to',
                        'topic_node': 'Greetings',
                    }
                )
            )
        )
        assert related_nodes == [
            MCQNode(name='Good Morning', info=''),
            MCQNode(name='Hey', info=''),
            MCQNode(name='Hola', info=''),
        ]

    def test_similarity_matrix(self, complex_graph: MCQGraph):
        """Tests the retrieval of a similarity matrix dictionary with similarity scores."""
        similarity_matrix = complex_graph.similarity_matrix(
            MCQNode(**{'name': 'Hello'})
        )
        assert similarity_matrix['Hey'] == 1.0
        assert similarity_matrix['Ciao'] == 0.25
