"""A utility module for MCQBot"""

import random
from typing import List, Optional, Tuple

from app.data.mcq_graph import MCQGraph
from app.models import MCQ, MCQRelationship
from app.utils.fake_word_generator import FakeWordGenerator


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
        answers = [x.name for x in self.graph.related_nodes(relationship)]

        # Exclusions are made up of all nodes that connect to the original answer node, as they are also valid topics.
        end_node = self.graph.get_node(name=relationship.end_node)
        exclusions = []
        if end_node:
            exclusions = [x.name for x in self.graph.connected_nodes(end_node)]

        # A similarity matrix is created using the nearby relationships in the graph to the answer node to find plausible distractors.
        similarities = list(
            self.graph.similarity_matrix(relationship)['Node2'].unique()
        )
        distractors = [
            x for x in similarities if x not in answers and x not in exclusions
        ]
        return answers, distractors

    def generate(self) -> MCQ:
        """
        Generate answer, topic and distractors.

        Returns:
            Dict[str, Union[str, List[str]]]:
        """
        relationship = self.graph.random_relationship(seed=self.seed)
        answer = relationship.end_node
        answers, distractors = self.__collect_nodes(relationship)

        # create a fake blended word
        fwg = FakeWordGenerator(pool=answers + distractors)
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
            answer=answer, topic=relationship.start_node, choices=choices
        )
