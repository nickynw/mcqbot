import logging
import os

import pytest
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship
from dotenv import load_dotenv

logging.getLogger('neo4j.bolt').setLevel(logging.DEBUG)

sample_properties = [{'name': 'Sample Node 1'}, {'name': 'Sample Node 2'}]


@pytest.fixture
def graph():
    load_dotenv()
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_user = os.getenv('NEO4J_USERNAME')
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    graph = MCQGraph(neo4j_uri, neo4j_user, neo4j_password)
    yield graph
    graph.delete_all()
    graph.close()


@pytest.fixture
def sample_graph(graph):
    graph.create_nodes([MCQNode(**node) for node in sample_properties])
    yield graph


class TestMCQGraph:
    def test_has_name(self, graph):
        with graph.driver.session() as session:
            node = {'name': 'Sample Node 0'}
            session.run('CREATE (:Entity $prop)', prop=node)
        assert graph.has_name('Sample Node 0')

    def test_create_nodes(self, graph):
        graph.create_nodes([MCQNode(**node) for node in sample_properties])
        for properties in sample_properties:
            assert graph.has_name(properties['name']) == MCQNode(**properties)

    def test_delete_all(self, sample_graph):
        sample_graph.delete_all()
        for properties in sample_properties:
            assert sample_graph.has_name(properties['name']) == None

    def test_relationships(self, sample_graph):
        relationship = MCQRelationship(
            **{
                'start_node': 'Sample Node 1',
                'type': 'is_linked_to',
                'end_node': 'Sample Node 2',
            }
        )
        assert sample_graph.has_relationship(relationship) == False
        sample_graph.create_relationships([relationship])
        assert sample_graph.has_relationship(relationship) == True

    def test_duplicate_input(self, graph):
        duplicate_properties = [
            {'name': 'Sample Node 1'},
            {'name': 'Sample Node 2'},
            {'name': 'Sample Node 2'},
        ]
        with pytest.raises(ValueError):
            graph.create_nodes(
                [MCQNode(**node) for node in duplicate_properties]
            )

    def test_duplicate_creation(self, sample_graph):
        duplicate_properties = [{'name': 'Sample Node 2'}]
        with pytest.raises(ValueError):
            sample_graph.create_nodes(
                [MCQNode(**node) for node in duplicate_properties]
            )
