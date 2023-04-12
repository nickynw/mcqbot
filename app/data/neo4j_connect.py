from typing import List, Optional, Tuple
from py2neo import Graph, Node, Relationship, Transaction
from app.models import MCQNode, MCQRelationship
from app.utils.log_util import create_logger
from py2neo.bulk import create_nodes, create_relationships

logger = create_logger(__name__)

class MCQGraph():
    """Class provides a data access layer to the Neo4J Graph Database"""
    def __init__(self, uri: str, username: str, password: str):
        self.__graph = Graph(uri, auth=(username, password))
        self.batch_size = 500

    def delete_all(self):
        """
        Cleares all data from the database.
        """
        self.__graph.delete_all()

    def create(self, nodes: Optional[MCQNode] = None, relationships: Optional[MCQRelationship] = None):
        """
        Creates nodes and relationships in the connected Neo4J database

        Args:
            nodes (Optional[MCQNode]): List of nodes to create
            relationships (Optional[MCQRelationship]): List of relationships to create
        """
        tx = self.__graph.begin()

        if nodes:
            for i in range(0, len(nodes), self.batch_size):
                node_batch = nodes[i:i +  self.batch_size]
                node_summary = create_nodes(tx, [x.dict() for x in node_batch])

                print(f"Created {node_summary.nodes_created} nodes")

        if relationships:
            for i in range(0, len(relationships), self.batch_size):
                rel_batch = relationships[i:i +  self.batch_size]
                create_nodes(tx, [x.dict() for x in rel_batch])

        self.__graph.commit(tx)