"""A utility module for MCQBot"""

import itertools
import random
from typing import Generator, List, Tuple, Union

import Levenshtein
import pyphen


class FakeWordGenerator:
    """
    This module contains code for a FakeWordGenerator, which aims to generate plausible fake words.
    It achieves this by hyphenating an input list of words and generating permutations that are similar to the input words.
    """

    dic_US = pyphen.Pyphen(lang='en_US')
    dic_GB = pyphen.Pyphen(lang='en_GB')

    def __init__(self, words: List[str]):
        self.pool = words
        self.second_parts = [
            x[1]
            for x in list(
                itertools.chain.from_iterable(
                    self.__split_pairs(word) for word in self.pool
                )
            )
        ]

    @staticmethod
    def __is_valid_word(a: str, b: str) -> bool:
        """
        Checks whether a fake constructed word appears valid based on consonant/vowel combination conventions.

        Args:
            a (str): first part of the word
            b (str): second part of the word

        Returns:
            bool
        """

        if len(a) == 0 or len(b) == 0:
            return False

        vowels = 'aeiou'

        # Return True for vowel then consonant or consonant then vowel at word break
        if (a[-1] in vowels) != (b[0] in vowels):
            return True

        # Return True for double consonants followed by a vowel at word break
        if (
            len(b) > 1
            and a[-1] not in vowels
            and b[0] not in vowels
            and b[1] in vowels
        ):
            return True

        return False

    @staticmethod
    def __similarity_score(a: str, b: str) -> float:
        """
        Calculates the similarity score between two strings using the Levenshtein distance algorithm.

        Args:
            a (str): first string
            b (str): second string

        Returns:
            float: levenshtein distance score
        """
        distance = Levenshtein.distance(a.lower(), b.lower())
        max_length = max(len(a), len(b))
        return 1 - distance / max_length

    @staticmethod
    def __split_pairs(word: str) -> List[Tuple[str, str]]:
        """
        Splits words into possible pairings, e.g. dopamine to dopa-mine and extended to include dop-amine.

        Args:
            word (str): the input word to find split word pairs for

        Returns:
            List[Tuple[str, str]]: A list of generated pairs of ways a word can be split
        """
        pairs = list(FakeWordGenerator.dic_US.iterate(word))
        if not pairs:
            pairs = list(FakeWordGenerator.dic_GB.iterate(word))

        # Adds permutations of consonant/vowels around the split location.
        pairs.extend(
            [
                (pair[0][:-1], pair[0][-1] + pair[1])
                for pair in pairs
                if pair[0][-1] not in 'aeiou' and pair[1][0] in 'aeiou'
            ]
        )

        return pairs if len(pairs) > 0 else [(word, '')]

    def __find_match(
        self, potential_fakes: Generator, threshold: float
    ) -> Generator:
        """
        A generator that yields a generated fake word above a similarity score threshold when compared to all original input words.
        Generators are used to iterate over possible permutations without loading all of them into memory at once.

        Args:
            fake_words (Generator[str, None, None]): potential new words
            existing_words (List[str]): the full original list of words
            threshold (float): the score threshold for similarity to accept

        Returns:
            Generator[str]: a fake word generator

        Yields:
            str: a fake word
        """

        random.shuffle(self.pool)

        for fake_word, word in itertools.product(potential_fakes, self.pool):
            if (
                FakeWordGenerator.__similarity_score(fake_word, word)
                > threshold
            ):
                yield fake_word

    def generate(
        self,
        limit: int = 1,
        threshold: float = 0.6,
        exclude: Union[List[str], None] = None,
    ) -> List[str]:
        """Given a set of input words and n, generate n number of new fake words with a similarity score higher than the threshold to any of the original words.

        Args:
            limit (int, optional): limit the number of words generated, is capped at the total length of original input words
            threshold (float, optional): The threshold score between 0-1 to accept fake words in similarity to existing words. Defaults to 0.6.
            exclude (List[str], optional): any words to exclude as a base when generating new words, Defaults to [].

        Returns:
            List[str]: a list of plausible fake words
        """

        output = []

        if exclude:
            subpool = [x for x in self.pool if x not in exclude]
            input_words = random.sample(subpool, min(len(subpool), limit))
        else:
            input_words = random.sample(self.pool, min(len(self.pool), limit))

        for word in input_words:
            random.shuffle(self.second_parts)
            random_word_pairs = self.__split_pairs(word)
            first_part = random.choice(random_word_pairs)[0]
            exceptions = [x[1] for x in random_word_pairs]

            potential_fakes = (
                first_part + second_part
                for second_part in self.second_parts
                if second_part not in exceptions
                and first_part + second_part not in self.pool
                and self.__is_valid_word(first_part, second_part)
            )

            fake_word = next(
                (x for x in self.__find_match(potential_fakes, threshold)),
                None,
            )
            if fake_word:
                output.append(fake_word)

        return output
