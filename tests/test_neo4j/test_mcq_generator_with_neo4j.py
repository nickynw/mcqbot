"""Test the MCQGenerator Class using a Neo4J Graph Database"""
import os

import pytest
from app.data.neo4j_graph import Neo4JGraph
from app.models import MCQ
from app.utils.mcq_generator import MCQGenerator
from dotenv import load_dotenv

load_dotenv()
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_password = os.getenv('NEO4J_PASSWORD')


@pytest.mark.parametrize(
    'test_graph',
    [Neo4JGraph(neo4j_uri, 'neo4j', neo4j_password)],
    indirect=True,
)
def test_mcq_generator_with_neo4j(test_graph):
    """A test to show that the MCQ generator is working correctly."""
    mcq = MCQGenerator(test_graph, seed=3)
    output = mcq.generate()
    assert output == MCQ(
        answer='English',
        topic='Greetings',
        choices=['Goodyou later', 'English', 'Ciao', 'Adios'],
    )
