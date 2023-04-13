from typing import Dict, List, Optional, Tuple
from py2neo import Graph, Node, Relationship, Transaction, NodeMatcher, RelationshipMatcher
from app.models import MCQNode, MCQRelationship
from app.utils.log_util import create_logger
from py2neo.bulk import create_nodes, create_relationships
from collections import Counter

logger = create_logger(__name__)

class MCQGraph():
    """Class provides a data access layer to the Neo4J Graph Database"""
    def __init__(self, uri: str, username: str, password: str):
        self.graph = Graph(uri, auth=(username, password))
        self.batch_size = 500
        logger.info('New MCQGraph Object created - connection opened.')

    def delete_all(self):
        """
        Cleares all data from the database.
        """
        self.graph.delete_all()
        logger.info(f'All nodes removed from graph database.')

    def create_nodes(self, nodes: List[MCQNode]):
        """
        Uses py2neo create_nodes bulk function, which unfortunately does not return anything.
        Instead we log any input nodes that are skipped.

        Args:
            nodes (List[MCQNode]): _description_

        Raises:
            ValueError: _description_
        """
        # Warn if there are duplicate names
        counter = Counter([x.name for x in nodes])
        duplicates = [x for x in nodes if counter[x.name] > 1]

        if duplicates:
            logger.warn(f'Duplicate names detected: %s', {x.name for x in nodes}, extra={'nodes':duplicates})
            raise ValueError("Duplicates discovered within input nodes by name. Please remove these before reattempting bulk creation.")
                        
        # Create bulk nodes in batches, keep track of nodes skipped due to pre-existing node.
        skipped_nodes = []
        for i in range(0, len(nodes), self.batch_size):
            node_batch = [x for x in nodes[i:i +  self.batch_size]]
            skip_batch = [x for x in node_batch if bool(self.match_nodes([{'name':x.name}], log = False))]
            skipped_nodes.extend(skip_batch)
            create_nodes(self.graph.auto(), [x.dict() for x in node_batch if x not in skip_batch])

        if skipped_nodes:
            logger.warn(f'Skipped nodes that already exist with these names: %s', {x.name for x in skipped_nodes}, extra={'nodes':skipped_nodes})

        logger.info(f'{len(nodes)-len(skipped_nodes)} nodes created out of {len(nodes)}.')

    def create_relationships(self, relationships: List[MCQRelationship]):
        for i in range(0, len(relationships), self.batch_size):
            rel_batch = relationships[i:i +  self.batch_size]
            create_relationships(self.graph.auto(), [x.dict() for x in rel_batch])
    
        logger.info(f'{len(relationships)} relationships created.')

    def match_nodes(self, properties: List[Dict[str, str]], log: bool = True) -> List[MCQNode]:
        matcher = NodeMatcher(self.graph)
        output = []

        for prop in properties:
            result = matcher.match(**prop).first()
            if result:  
                output.append(MCQNode.from_node(result))
    
        if log:
            logger.info(f'Found {len(output)} matches from {len(properties)} properties provided.')
        return output

    def match_relationships(self, relationships: List[MCQRelationship]) -> List[MCQRelationship]:
        matcher = RelationshipMatcher(self.graph)
        output = []

        for rel in relationships:
            result = matcher.match(**rel).first()
            if result:  
                output.append(MCQRelationship.from_relationship(result))
    
        return output
              
    #TODO: assert on logger, look into what happens if node creation fails in bulk. how to run in github action