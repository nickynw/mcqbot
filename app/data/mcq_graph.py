"""Object for acessing neo4j graph database"""
from typing import List, Union

from app.models import MCQNode, MCQRelationship
from app.utils.log_util import create_logger

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

    def has_name(self, name: str) -> Union[MCQNode, None]:
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
