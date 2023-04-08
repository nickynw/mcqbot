"""A utility module for MCQBot"""

import random
from typing import Dict, List, Tuple, Union

import networkx as nx
from fake_word_generator import FakeWordGenerator


class MCQGenerator:
    """A class for generating a topic, answer and choices from a graph"""

    def __init__(self, graph: nx.DiGraph):
        self.graph = graph
        self.edges = list(self.graph.edges())

    def __collect_nodes(
        self, answer: str, topic: str
    ) -> Tuple[List[str], List[str]]:
        """
        Collects nearby nodes and neighbours to determine distractors and all answers for given topic.

        Args:
            answer (str): the answer side of an edge
            topic (str): the topic side of an edge

        Returns:
            Tuple[List[str], List[str]]: A list of all possible answers to a question and plausible distractors
        """
        answers = [x[1] for x in self.edges if x[0] == topic]
        exceptions = nx.all_neighbors(self.graph, answer)
        similarities = nx.simrank_similarity(self.graph, source=answer)
        distractors = [
            x for x in similarities if x not in answers and x not in exceptions
        ]
        return answers, distractors

    def generate(self) -> Dict[str, Union[str, List[str]]]:
        """
        Generate answer, topic and distractors.

        Returns:
            Dict[str, Union[str, List[str]]]:
        """
        topic, answer = random.choice(self.edges)
        answers, distractors = self.__collect_nodes(answer, topic)
        pool = answers + distractors
        fwg = FakeWordGenerator(pool)
        distractors = random.sample(distractors, 2)
        fake = fwg.generate(exclude=[answer] + distractors, limit=1).pop()
        choices = [answer] + distractors + [fake]
        random.shuffle(choices)
        return {'topic': topic, 'answer': answer, 'choices': choices}
