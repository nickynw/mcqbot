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


class MCQRelationship(BaseModel):
    """Model for Nodes in Neo4J"""

    node_a: str
    rel_type: str
    node_b: str
    
    class Config:
        extra = 'forbid'

