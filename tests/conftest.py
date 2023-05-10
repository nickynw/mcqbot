"""Provides fixtures shared between different test files."""
from typing import Dict, Generator, List

import pytest
from api.data.mcq_graph import MCQGraph
from api.models import MCQNode, MCQRelationship
from tests.test_utils import fill_graph


@pytest.fixture(name='complex_graph')
def complex_graph_fixture(
    graph: MCQGraph, test_data: Dict[str, List[str]]
) -> Generator[MCQGraph, None, None]:
    """
    Populates the database with sample nodes.

    Args:
        graph (Generator[MCQGraph]): An empty databases and MCQGraph driver.

    Yields:
        Generator[MCQGraph]: A database populated with sample nodes.
    """
    yield fill_graph(graph, test_data)


@pytest.fixture(name='test_data')
def test_data_fixture():
    """Provides data for a simple graph using common words and phrases"""
    data = {
        'Blah': [],
        'Hello': [],
        'Hey': [],
        'Good Morning': [],
        'Hola': [],
        'Greetings': ['Hello', 'Hey', 'Good Morning', 'Hola'],
        'Goodbye': [],
        'Adios': [],
        'Ciao': [],
        'Farewells': ['Adios', 'Ciao', 'Goodbye', 'See you later'],
        'See you later': [],
        'English': [
            'Hello',
            'Hey',
            'Good Morning',
            'Goodbye',
            'See you later',
            'Greetings',
            'Farewells',
        ],
        'Words': [
            'Hello',
            'Hey',
            'Good Morning',
            'Goodbye',
            'See you later',
            'Greetings',
            'Farewells',
            'Adios',
            'Ciao',
            'Hola',
            'English',
            'Blah',
        ],
    }
    return data


@pytest.fixture(name='simple_properties')
def simple_properties_fixture() -> List[Dict[str, str]]:
    """A list of simple properties to use for node creation and validation."""
    return [{'name': 'Sample Node 1'}, {'name': 'Sample Node 2'}]


@pytest.fixture(name='simple_graph')
def simple_graph_fixture(
    graph: MCQGraph, simple_properties: List[Dict[str, str]]
) -> Generator[MCQGraph, None, None]:
    """
    Populates the database with sample nodes.

    Args:
        graph (Generator[MCQGraph]): An empty databases and MCQGraph driver.

    Yields:
        Generator[MCQGraph]: A database populated with sample nodes.
    """

    graph.create_nodes([MCQNode(**node) for node in simple_properties])
    yield graph


@pytest.fixture(name='simple_relationships_graph')
def simple_relationships_graph_fixture(
    simple_graph: MCQGraph,
) -> Generator[MCQGraph, None, None]:
    """Provides a simple graph with simple relationships between the nodes"""
    relationships = [
        MCQRelationship(
            **{
                'answer_node': 'Sample Node 1',
                'type': 'is_linked_to',
                'topic_node': 'Sample Node 2',
            }
        ),
        MCQRelationship(
            **{
                'answer_node': 'Sample Node 2',
                'type': 'is_linked_to',
                'topic_node': 'Sample Node 1',
            }
        ),
    ]
    simple_graph.create_relationships(relationships)
    yield simple_graph
