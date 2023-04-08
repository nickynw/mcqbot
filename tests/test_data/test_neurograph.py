"""Test the creation of the sample graph is working as intended"""
from app.data.neurograph import create_graph, data


def test_graph():
    """Test the creation of the sample graph is working as intended"""
    graph = create_graph()
    assert len(graph.nodes()) == len(data)
    print(graph.edges())
