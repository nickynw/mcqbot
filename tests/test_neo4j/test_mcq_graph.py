"""Test the MCQGraph class object interface with Neo4J Database, are operations working as expected"""
import logging
import os
from typing import Generator

import pytest
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship
from dotenv import load_dotenv

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)

sample_properties = [{'name': 'Sample Node 1'}, {'name': 'Sample Node 2'}]


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
    graph = MCQGraph(neo4j_uri, 'neo4j', neo4j_password)
    yield graph
    graph.delete_all()
    graph.close()


@pytest.fixture(name='sample_graph')
def sample_graph_fixture(graph: MCQGraph) -> Generator[MCQGraph, None, None]:
    """
    Populates the database with sample nodes.

    Args:
        graph (Generator[MCQGraph]): An empty databases and MCQGraph driver.

    Yields:
        Generator[MCQGraph]: A database populated with sample nodes.
    """
    graph.create_nodes([MCQNode(**node) for node in sample_properties])
    yield graph


class TestMCQGraph:
    """Test class for MCQGraph"""

    def test_has_name(self, graph: MCQGraph):
        """Tests whether the has_name function can successfully check a node exists."""
        with graph.driver.session() as session:
            node = {'name': 'Sample Node 0'}
            session.run('CREATE (:Entity $prop)', prop=node)
        assert graph.has_name('Sample Node 0')

    def test_create_nodes(self, graph: MCQGraph):
        """Tests whether the create node function successfully created sample nodes and checks they exist."""
        graph.create_nodes([MCQNode(**node) for node in sample_properties])
        for properties in sample_properties:
            assert graph.has_name(properties['name']) == MCQNode(**properties)

    def test_delete_all(self, sample_graph: MCQGraph):
        """Tests whether the delete_all function succesfully deletes the nodes we created."""
        sample_graph.delete_all()
        for properties in sample_properties:
            assert sample_graph.has_name(properties['name']) is None

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
