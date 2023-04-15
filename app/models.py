"""One file to store models for pydantic, no linting for this file as it doesnt follow a lot conventions."""
# pylint: skip-file

from typing import List

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

    def __lt__(self: 'MCQNode', other: 'MCQNode'):
        return self.name < other.name


class MCQRelationship(BaseModel):
    """Model for Nodes in Neo4J"""

    start_node: str
    type: str
    end_node: str

    class Config:
        extra = 'forbid'
