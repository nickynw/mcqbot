"""Object for acessing neo4j graph database"""
from collections import Counter
from typing import List, Union

import networkx as nx
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship
from app.utils.log_util import create_logger

logger = create_logger(__name__)


class NXGraph(MCQGraph):
    """
    This object forms a data access layer via neo4j python driver to the neo4j graph database.
    """

    def __init__(self):
        super()
        self.graph = nx.DiGraph()
        logger.info('New networkx graph object created.')

    def delete_all(self):
        self.graph.clear()

    def create_nodes(self, nodes: List[MCQNode]):
        # Check for duplicates within the input
        counter = Counter([node.name for node in nodes])
        duplicates = [node for node in nodes if counter[node.name] > 1]
        if duplicates:
            logger.error(
                'Duplicate name inputs detected: %s',
                {node.name for node in nodes},
                extra={'nodes': duplicates},
            )
            raise ValueError(
                f'Duplication Error: {len(duplicates)} node duplicates within input.'
            )

        # Check for duplicates within the database
        matches = [node for node in nodes if self.graph.has_node(node.name)]
        if matches:
            logger.error(
                'Nodes already exist with these names: %s',
                {node.name for node in matches},
                extra={'nodes': matches},
            )
            raise ValueError(
                f'Duplication Error: {len(matches)} nodes already have names in database.'
            )

        # Create nodes in session batches
        for node in nodes:
            self.graph.add_node(node.name, **node.dict())
        logger.info('Created %s nodes.', len(nodes))

    def create_relationships(self, relationships: List[MCQRelationship]):
        for relationship in relationships:
            try:
                self.graph.add_edge(
                    relationship.start_node,
                    relationship.end_node,
                    type=relationship.type,
                )
            # pylint: disable=broad-except
            except Exception as e:
                logger.warning(
                    'Failed to create relationship: %s',
                    str(relationship),
                    extra={'exception': e},
                )
        logger.info(
            'Created %s relationships in the database.', len(relationships)
        )

    def has_name(self, name: str) -> Union[MCQNode, None]:
        if self.graph.has_node(name):
            return MCQNode(**self.graph.nodes[name])
        return None

    def has_relationship(self, relationship: MCQRelationship) -> bool:
        for start_node, end_node, props in self.graph.edges(data=True):
            if (
                start_node == relationship.start_node
                and end_node == relationship.end_node
                and props['type'] == relationship.type
            ):
                return True
        return False
