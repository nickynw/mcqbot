"""Object for acessing neo4j graph database"""
import random
from collections import Counter
from typing import List, Optional, Union

import networkx as nx
import pandas as pd
from app.data.mcq_graph import MCQGraph
from app.models import MCQNode, MCQRelationship
from app.utils.log_util import create_logger

logger = create_logger(__name__)


class NXGraph(MCQGraph):
    """
    This object stores and pulls data from  a local graph database object in memory, as opposed to a seperate database.
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

    def get_node(self, name: str) -> Union[MCQNode, None]:
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

    def related_nodes(self, relationship: MCQRelationship) -> List[MCQNode]:
        return [
            MCQNode(**self.graph.nodes[relationship.end_node])
            for x in self.graph.edges
            if x[0] == relationship.start_node
        ]

    def connected_nodes(self, node: MCQNode) -> List[MCQNode]:
        nodes = nx.ego_graph(self.graph, node.name, radius=1, undirected=True)
        nodes = [MCQNode(**self.graph.nodes[x]) for x in nodes]
        return nodes

    def random_relationship(
        self, seed: Optional[int] = None
    ) -> MCQRelationship:
        if seed:
            random.seed(seed)
        edge = random.choice(list(self.graph.edges))
        edge_data = self.graph.get_edge_data(*edge)
        return MCQRelationship(
            start_node=edge[0], end_node=edge[1], **edge_data
        )

    def similarity_matrix(self, relationship: MCQRelationship) -> pd.DataFrame:
        node = relationship.end_node
        subgraph = nx.ego_graph(self.graph, node, radius=4, undirected=True)
        answer_nodes = [
            x[1] for x in subgraph.edges if x[0] == relationship.start_node
        ]
        output = {}
        for answer_node in answer_nodes:
            output[answer_node] = nx.simrank_similarity(
                subgraph, source=answer_node
            )

        df = pd.DataFrame(output)
        df['Node1'] = df.index
        df = pd.melt(
            df,
            id_vars=['Node1'],
            value_vars=list(df.columns),
            var_name='Node2',
            value_name='similarity',
        )
        df = df[df['Node1'] != df['Node2']]
        df = df.sort_values('similarity', ascending=False)
        return df
