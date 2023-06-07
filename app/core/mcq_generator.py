"""A utility module for MCQBot"""

import random
from typing import List, Optional, Tuple

from app.core.fake_word_generator import FakeWordGenerator
from app.graphs.mcq_graph import MCQGraph
from app.models import MCQ, MCQRelationship


class MCQGenerator:
    """A class for generating a topic, answer and choices from a graph
    An edge is chosen (e.g. Sam -> Person), Sam is an 'answer', Person is a 'topic', all other valid answers are found and excluded.
    Then similar nodes that share qualities with those answers are gathered as the 'distractors'.
    Nodes are also pooled and if possible fake blended words are created from those too.

    """

    def __init__(self, graph: MCQGraph, seed: Optional[int] = None):
        self.graph = graph
        self.seed = seed

    def __collect_nodes(
        self, relationship: MCQRelationship
    ) -> Tuple[List[str], List[str]]:
        """
        Collects nearby nodes and neighbours to determine distractors and all potential correct answers for given topic/edge.

        Args:
            answer (str): the answer side of an edge
            topic (str): the topic side of an edge

        Returns:
            Tuple[List[str], List[str]]: A list of all possible answers to a question and plausible distractors
        """
        # Answers are all other nodes that connect to this given topic in the same direction.
        answer_nodes = [x.name for x in self.graph.related_nodes(relationship)]
        answer_node = self.graph.get_node(name=relationship.answer_node)
        if answer_node is None:
            raise ValueError(
                'Unable to find randomly selected answer node in database.'
            )

        # Nodes to exclude from distractors include any connected nodes to the chosen answer node
        exclusions = [x.name for x in self.graph.connected_nodes(answer_node)]

        # Distractors are taken from nodes with high similarity near to the chosen answer node
        similar_nodes = sorted(self.graph.similarity_matrix(answer_node))

        distractors = [
            x
            for x in similar_nodes
            if x not in answer_nodes
            and x not in exclusions
            and x != relationship.answer_node
            and x != relationship.topic_node
        ]
        return answer_nodes, distractors

    def generate(self) -> MCQ:
        """
        Generate answer, topic and distractors.

        Returns:
            Dict[str, Union[str, List[str]]]:
        """
        relationship = self.graph.random_relationship(seed=self.seed)
        answer = relationship.topic_node
        answers, distractors = self.__collect_nodes(relationship)

        # create a fake blended word
        fwg = FakeWordGenerator(pool=answers + distractors, seed=self.seed)
        fakes = fwg.generate(filter_list=[answer] + distractors, limit=1)

        # shuffle the answer, distractors and fakes
        random.seed(self.seed)
        distractors = (
            distractors
            if len(distractors) < 2
            else random.sample(distractors, 2)
        )

        choices = [answer] + distractors + fakes
        random.seed(self.seed)
        random.shuffle(choices)
        return MCQ(
            answer=answer, topic=relationship.answer_node, choices=choices
        )
