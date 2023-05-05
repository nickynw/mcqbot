"""A template to test that all of the MCQGraph class object interface operations working as expected"""
import logging
from typing import Dict, List

import pytest
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship

pytestmark = pytest.mark.skip(
    reason='This module is not meant to be run directly, it is a template.'
)

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)


class TestMCQGraph:
    """Test class for MCQGraph Base Class containing tests to run on all inheriting classes."""

    def test_has_name(self, single_node_graph: MCQGraph):
        """Tests whether the has_name function can successfully check a node exists."""
        assert single_node_graph.get_node('Sample Node 0')

    def test_create_nodes(
        self, graph: MCQGraph, simple_properties: List[Dict[str, str]]
    ):
        """Tests whether the create node function successfully created sample nodes and checks they exist."""
        graph.create_nodes([MCQNode(**node) for node in simple_properties])
        for properties in simple_properties:
            assert graph.get_node(properties['name']) == MCQNode(**properties)

    def test_delete_all(
        self, simple_graph: MCQGraph, simple_properties: List[Dict[str, str]]
    ):
        """Tests whether the delete_all function succesfully deletes the nodes we created."""
        simple_graph.delete_all()
        for properties in simple_properties:
            assert simple_graph.get_node(properties['name']) is None

    def test_duplicate_input(self, graph: MCQGraph):
        """Tests whether an error is raised when we use duplicated input to create nodes"""
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
        """Tests whether an error is raised when we attempt to create a node that already exists"""
        duplicate_properties = [{'name': 'Sample Node 2'}]
        with pytest.raises(ValueError):
            simple_graph.create_nodes(
                [MCQNode(**node) for node in duplicate_properties]
            )

    def test_relationships(self, simple_graph: MCQGraph):
        """Tests whether we can create relationships and checks if they fail."""
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
        """Tests whether we can grab a random relationship with different random seeds"""
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
        """Tests whether we correctly retrieve the nodes connected to another node"""

        connected_nodes = sorted(
            complex_graph.connected_nodes(MCQNode(**{'name': 'Hello'}))
        )
        assert connected_nodes == [
            MCQNode(name='English', info=''),
            MCQNode(name='Greetings', info=''),
            MCQNode(name='Words', info=''),
        ]

    def test_related_nodes(self, complex_graph: MCQGraph):
        """Tests whether we correctly retrieve the nodes connected to another node"""
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
        """Tests whether we correctly retrieve the nodes connected to another node"""
        similarity_matrix = complex_graph.similarity_matrix(
            MCQNode(**{'name': 'Hello'})
        )
        assert similarity_matrix['Hey'] == 1.0
        assert similarity_matrix['Ciao'] == 0.25
