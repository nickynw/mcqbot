"""A template to test that all of the MCQGraph class object interface operations working as expected"""
import logging

import pytest
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship

pytestmark = pytest.mark.skip(
    reason='This module is not meant to be run directly, it is a template.'
)

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)

sample_properties = [{'name': 'Sample Node 1'}, {'name': 'Sample Node 2'}]


class TestMCQGraph:
    """Test class for MCQGraph Base Class containing tests to run on all inheriting classes."""

    def test_has_name(self, single_node_graph: MCQGraph):
        """Tests whether the has_name function can successfully check a node exists."""
        assert single_node_graph.get_node('Sample Node 0')

    def test_create_nodes(self, graph: MCQGraph):
        """Tests whether the create node function successfully created sample nodes and checks they exist."""
        graph.create_nodes([MCQNode(**node) for node in sample_properties])
        for properties in sample_properties:
            assert graph.get_node(properties['name']) == MCQNode(**properties)

    def test_delete_all(self, sample_graph: MCQGraph):
        """Tests whether the delete_all function succesfully deletes the nodes we created."""
        sample_graph.delete_all()
        for properties in sample_properties:
            assert sample_graph.get_node(properties['name']) is None

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

    def test_duplicate_creation(self, sample_graph: MCQGraph):
        """Tests whether an error is raised when we attempt to create a node that already exists"""
        duplicate_properties = [{'name': 'Sample Node 2'}]
        with pytest.raises(ValueError):
            sample_graph.create_nodes(
                [MCQNode(**node) for node in duplicate_properties]
            )

    def test_relationships(self, sample_graph):
        """Tests whether we can create relationships and checks if they fail."""
        relationship = MCQRelationship(
            **{
                'start_node': 'Sample Node 1',
                'type': 'is_linked_to',
                'end_node': 'Sample Node 2',
            }
        )
        assert sample_graph.has_relationship(relationship) is False
        sample_graph.create_relationships([relationship])
        assert sample_graph.has_relationship(relationship) is True
