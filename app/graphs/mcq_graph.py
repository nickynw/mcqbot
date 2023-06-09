"""Object for acessing neo4j graph database"""
from typing import Dict, List, Optional, Union

from app.graphs.log_util import create_logger
from app.models import MCQNode, MCQRelationship

logger = create_logger(__name__)


class MCQGraph:
    """
    This is a baseclass for the interface used by other modules to interact with graph databases.
    """

    def __init__(self):
        pass

    def close(self):
        """Ensure all connections are closed where appropriate."""

    def delete_all(self):
        """Deletes all nodes in the database."""

    def create_nodes(self, nodes: List[MCQNode]):
        """
        Creates nodes in the database using a list of input nodes with expected properties.

        Args:
            nodes (List[MCQNode]): input nodes.

        Raises:
            ValueError: Raised if any form of duplication can occur on node name.
        """

    def create_relationships(self, relationships: List[MCQRelationship]):
        """
        Creates relationships given a list of input relationships.

        Args:
            relationships (List[MCQRelationship]): list of relationships to create

        Raises:
            ValueError: if a relationship fail to be created.
        """

    def get_node(self, name: str) -> Union[MCQNode, None]:
        """
        Checks the database contains a node with the given name.

        Args:
            name (str): name to check against

        Returns:
            MCQNode: the node found with the given name
        """
        raise NotImplementedError()

    def has_relationship(self, relationship: MCQRelationship) -> bool:
        """
        Checks if database has the provided relationship.

        Args:
            relationship (MCQRelationship): The relationship to check for.

        Returns:
            bool: bool representation of found relationship in database.
        """
        raise NotImplementedError()

    def random_relationship(
        self, seed: Optional[int] = None
    ) -> MCQRelationship:
        """
        Randomly choose and return a relationship

        Returns:
            MCQRelationship: randomly chosen relationship
        """
        raise NotImplementedError()

    def related_nodes(self, relationship: MCQRelationship) -> List[MCQNode]:
        """
        Based on a given relationship, provide all related nodes with the same relationship to the start node

        Args:
            relationship (MCQRelationship): input relationship

        Returns:
            List[MCQNode]: List of related nodes
        """
        raise NotImplementedError()

    def connected_nodes(self, node: MCQNode) -> List[MCQNode]:
        """
        Provides all nodes connected to the given node

        Args:
            node (MCQNode): input node

        Returns:
            List[MCQNode]: list of all connected nodes
        """
        raise NotImplementedError()

    def similarity_matrix(self, node: MCQNode) -> Dict[str, float]:
        """_summary_

        Args:
            node (MCQNode): input node to get similarity for

        Returns:
            Dict[str, float]: simlarity values for each node key
        """
        raise NotImplementedError()

    def fill_graph(self, data: Dict[str, List[str]]):
        """
        Fills graph with provided dictionary input

        Args:
            data (Dict[str, List[str]]): input data

        """
        found_nodes = set()
        relationships = []
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    found_nodes.add(key)
                    found_nodes.add(item)
                    relationships.append(
                        MCQRelationship(
                            **{
                                'answer_node': key,
                                'topic_node': item,
                                'type': 'includes',
                            }
                        )
                    )
                    relationships.append(
                        MCQRelationship(
                            **{
                                'topic_node': key,
                                'answer_node': item,
                                'type': 'belongs_to',
                            }
                        )
                    )
        nodes = [MCQNode(**{'name': key}) for key in sorted(found_nodes)]
        self.delete_all()
        self.create_nodes(nodes=nodes)
        self.create_relationships(relationships=relationships)
