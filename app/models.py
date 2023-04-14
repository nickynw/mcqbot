"""One file to store models for pydantic, no linting for this file as it doesnt follow a lot conventions."""
# pylint: skip-file

from typing import List

from neo4j.graph import Node, Relationship
from pydantic import BaseModel


class MCQ(BaseModel):
    """Model for a standard multiple choice question object that can be passed around"""

    answer: str
    topic: str
    choices: List[str]

    class Config:
        extra = 'forbid'


class MCQNode(BaseModel):
    """Model for Nodes in Neo4J"""

    name: str

    class Config:
        extra = 'forbid'
        sort_key = 'name'

    @classmethod
    def from_node(cls, node: Node):
        return cls(**dict(node.items()))

    def __lt__(self: 'MCQNode', other: 'MCQNode'):
        return self.name < other.name


class MCQRelationship(BaseModel):
    """Model for Nodes in Neo4J"""

    start_node: str
    type: str
    end_node: str

    class Config:
        extra = 'forbid'

    @classmethod
    def from_relationship(cls, relationship: Relationship):
        return cls(**dict(relationship.items()))
