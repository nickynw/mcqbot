"""A utility module for MCQBot"""

import random
from typing import Dict, List, Tuple, Union

import networkx as nx
from app.utils.fake_word_generator import FakeWordGenerator


class MCQGenerator:
    """A class for generating a topic, answer and choices from a graph
    An edge is chosen (e.g. Sam -> Person), Sam is an 'answer', Person is a 'topic', all other valid answers are found and excluded.
    Then similar nodes that share qualities with those answers are gathered as the 'distractors'.
    Nodes are also pooled and if possible fake blended words are created from those too.

    """

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.edges = list(self.graph.edges())

    def __collect_nodes(
        self, answer: str, topic: str
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
        answers = [x[1] for x in self.edges if x[0] == topic]

        # Exclusions are made up of all nodes that connect to the original answer node, as they are also valid topics.
        exclusions = nx.all_neighbors(self.graph, answer)

        # A similarity matrix is created using the relationships in the graph to find nodes that form plausible distractors.
        similarities = nx.simrank_similarity(self.graph, source=answer)
        distractors = [
            x for x in similarities if x not in answers and x not in exclusions
        ]
        return answers, distractors

    def generate(self) -> Dict[str, Union[str, List[str]]]:
        """
        Generate answer, topic and distractors.

        Returns:
            Dict[str, Union[str, List[str]]]:
        """
        topic, answer = random.choice(self.edges)
        answers, distractors = self.__collect_nodes(answer=answer, topic=topic)

        # create a fake blended word
        fwg = FakeWordGenerator(pool=answers + distractors)
        fakes = fwg.generate(filter_list=[answer] + distractors, limit=1)

        # shuffle the answer, distractors and fakes
        choices = [answer] + random.sample(distractors, 2) + fakes
        random.shuffle(choices)
        return {'topic': topic, 'answer': answer, 'choices': choices}
