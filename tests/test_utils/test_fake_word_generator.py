"""Test the Fake Word Generator Class"""
import random

from app.utils.fake_word_generator import FakeWordGenerator


def test_fake_word_generator():
    """A test to show that the Fake Word Generator is able to generate plausible fake words."""
    random.seed(18)
    pool = ['Hello', 'Goodbye', 'Greetings']
    fwg = FakeWordGenerator(pool)
    output = fwg.generate(limit=3, threshold=0)
    assert output == {
        'Hello': 'Heltings',
        'Greetings': 'Greebye',
        'Goodbye': 'Goodlo',
    }
