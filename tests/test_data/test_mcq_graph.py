
import os
from dotenv import load_dotenv
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship
import pytest

sample_properties = [{'name':'Sample Node 1'}, {'name':'Sample Node 2'}]
sample_nodes = [MCQNode(**node) for node in sample_properties]

@pytest.fixture
def graph():
    load_dotenv()
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    graph = MCQGraph(neo4j_uri, neo4j_user, neo4j_password)
    yield graph
    graph.delete_all()

class TestMCQGraph:

    def test_create_nodes(self, graph):
        graph.create_nodes(sample_nodes)
        assert sorted(graph.match_nodes(sample_properties)) == sorted(sample_nodes)

    def test_delete_all(self, graph):
        graph.create_nodes(sample_nodes)
        graph.delete_all()
        assert graph.match_nodes(sample_properties) == []

    def test_create_relationships(self, graph):
        graph.create_nodes(sample_nodes)
        sample_relationships = [MCQRelationship(**{'node_a':'Sample Node 1', 'r_type':'is linked to', 'node_b':'Sample Node 2'})]
        graph.create_relationships(sample_relationships)
        assert sorted(graph.has_relationship()) == sorted(sample_nodes)